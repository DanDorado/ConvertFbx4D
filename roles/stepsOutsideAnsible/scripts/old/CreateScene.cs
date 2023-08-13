using UnityEngine;
using UnityEditor;
using System.Collections.Generic;
using UnityEditor.SceneManagement;
using UnityEngine.SceneManagement;
using System.IO;

// A Custom Tool to create new scenes with the 4d shapes imported as Megacache objects

// Button to import EVERYTHING into a scene per animation

// Button to import everything from an animation into a new scene

// Button to take the exact path of an animation and grab it.


public class CreateRoom : EditorWindow {

    // Default paths used to take in files
    string importLocation = "C:/Users/DanDo/OneDrive/Desktop/FinalFrames/ansibleexports";

    // Creates a toolbar, when selected implicitly calls ShowWindow()
    [MenuItem("DansCustomTools/Import New 4d Shapes")]
    private static void ShowWindow()
    {
        // Creates the main window, implicitly takes the content from OnGUI()
        var window = GetWindow<CreateRoom>();
        window.titleContent = new GUIContent("Import New 4d Shapes");
        window.Show();
    }

    // Defines shown content in window
    private void OnGUI()
    {
        // Default paths, can be changed
        importLocation = EditorGUILayout.TextField("Import Location", importLocation);

        // Once happy, pressing this will begin the creation of a new room and populating with the 4d items.
        if (GUILayout.Button("Import Everything"))
        {
            this.ImportAllTotal(importLocation);
        }
            
        if (GUILayout.Button("Close"))
            this.Close();
    }

    private void ImportAllTotal(string importLocation)
    {
        string dirPath = importLocation;

        this.ImportAllFromAnimation(importLocation);
        var SaveOK = EditorSceneManager.SaveScene(EditorSceneManager.GetActiveScene(), "Assets/Scenes/TestScene.unity");
    }


    private void ImportAllFromAnimation(string importLocation)
    {
        this.Import4DShape(importLocation);
    }

    // Use the TextureImporter to modify the texture to the correct settings
    private void Import4DShape(string importLocation)
    {
        //Gets the full path of where the .obj files are created by the ansible script.
        // Creates a Megacache object using the Megacache package.
        // Then makes the necessary changes I did manually before.
        // Currently not given any special coordinates.
        // Currently not able to actually import for some reason.
        //
        // It seems that instantiating the MegaCache Obj didn't allow the start script to run.
        // So I call it externally, which means I changed the script itself.
        // N.B. I changed MegaCacheOBJ.cs Start Script to be public.
        //
        // From: void Start()
        // To: public void Start()
        //


        string fullPath = importLocation;
        Debug.Log("Path is: "+fullPath);
        string[] objectFiles = Directory.GetFiles(fullPath);
        EditorApplication.ExecuteMenuItem("GameObject/Create Other/MegaCache/OBJ Cache");
        GameObject newMegaCache = GameObject.Find("Mega Cache Obj");

        newMegaCache.name="4DObject";
        Vector3 megaCacheObjectVector=newMegaCache.transform.position;
        newMegaCache.transform.position=new Vector3(0.0f, 1.1f, 0.0f);

        Vector3 megaCacheObjectScale=newMegaCache.transform.localScale;
        newMegaCache.transform.localScale=new Vector3(0.04f, 0.04f, 0.04f);

        Debug.Log(megaCacheObjectVector.x);

        Debug.Log(GameObject.Find("4DObject").transform.position);

        // newMegaCache.transform.position.z=(newMegaCache.transform.position.z+(1.0f*i));

        var megaCacheComponent=newMegaCache.GetComponent<MegaCacheOBJ>();
        megaCacheComponent.Start();
        megaCacheComponent.fps=10.0f;

        int fCount = Directory.GetFiles(fullPath, "*", SearchOption.TopDirectoryOnly).Length;

        megaCacheComponent.lastframe=(fCount-1);
        megaCacheComponent.animate=true;
        

        //MeshFilter my_mf=(MeshFilter)newMegaCache.GetComponent<MeshFilter>();
        MeshRenderer my_mr=(MeshRenderer)newMegaCache.GetComponent<MeshRenderer>();

        var mat = AssetDatabase.GetBuiltinExtraResource<Material>("Default-Material.mat");

        my_mr.sharedMaterial = mat;


        Material[] sharedMaterialsCopy = new Material[2];
        sharedMaterialsCopy[0] = mat;
        sharedMaterialsCopy[1] = mat;
        my_mr.sharedMaterials = sharedMaterialsCopy;

        string file = objectFiles[0];
        //string file = EditorUtility.OpenFilePanel("OBJ File", megaCacheComponent.lastpath, "obj");

		if ( file != null && file.Length > 1 )
		{
            //Debug.Log("I am going to try LOADOBJ");
			megaCacheComponent.lastpath = file;
			LoadOBJ(megaCacheComponent, file, megaCacheComponent.firstframe, megaCacheComponent.lastframe, megaCacheComponent.skip);
		}
    }



    public void LoadOBJ(MegaCacheOBJ mod, string filename, int first, int last, int step)
	{
		if ( mod.meshes.Count > 0 )
		{
			if ( !EditorUtility.DisplayDialog("Add to or Replace", "Add new OBJ meshes to existing list, or Replace All", "Add", "Replace") )
				mod.DestroyMeshes();
		}

		if ( step < 1 )
			step = 1;

		mod.InitImport();
		
        for ( int i = first; i <= last; i += step ){
            mod.LoadMtl(filename, i);
            //Debug.Log("Loaded "+i);
        }

		for ( int i = first; i <= last; i += step )
		{
			float a = (float)(i + 1 - first) / (last - first);
            //Debug.Log("Float is "+a);
			if ( !EditorUtility.DisplayCancelableProgressBar("Loading OBJ Meshes", "Frame " + i, a) )
			{
				Mesh ms = mod.LoadFrame(filename, i);
				if ( ms )
					mod.AddMesh(ms);
				else
				{
					EditorUtility.DisplayDialog("Can't Load File", "Could not load frame " + i + " of sequence! Import Stopped.", "OK");
					break;
				}
			}
			else
				break;
		}

        EditorUtility.ClearProgressBar();
    }
}
