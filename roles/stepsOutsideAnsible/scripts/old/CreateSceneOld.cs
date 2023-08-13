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
    string animationName = "3xFish_Cube.001";
    string exact4dShape =  "3xFish_Cube.001_KL_sAxis-0_oDis-1.1_rota-10.0_fr-200_HP-CoolHyperplane";

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
        animationName = EditorGUILayout.TextField("Animation", animationName);
        exact4dShape = EditorGUILayout.TextField("4d Shape", exact4dShape);

        // Once happy, pressing this will begin the creation of a new room and populating with the 4d items.
        if (GUILayout.Button("Import Everything"))
        {
            this.ImportAllTotal(importLocation);
        }
            
        // Needs doing, probably need to change the way the ansible script creates (or have it create a .txt file or something which contains tags)
        if (GUILayout.Button("Import all of animation"))
        {
            this.ImportAllFromAnimation(importLocation, animationName);
            var SaveOK = EditorSceneManager.SaveScene(EditorSceneManager.GetActiveScene(), "Assets/Scenes/"+animationName+".unity");
        }

        if (GUILayout.Button("Import an exact 4d Animation"))
        {
            // Creates a default room (eventually probably switch this to be empty once VR integrated, then runs an ImportShapeto create it)
            this.Import4DShape(importLocation, animationName, exact4dShape, 0);
            var SaveOK = EditorSceneManager.SaveScene(EditorSceneManager.GetActiveScene(), "Assets/Scenes/"+exact4dShape+".unity");
        }
        if (GUILayout.Button("Close"))
            this.Close();
    }

    private void ImportAllTotal(string importLocation)
    {
        string dirPath = importLocation;
        string[] dirs = Directory.GetDirectories(dirPath, "*", SearchOption.TopDirectoryOnly);

        foreach (string dir in dirs) 
        {
            Debug.Log(dir);
            Debug.Log(Path.GetFileName(dir));
            Debug.Log("3xFish_Cube.001");
            string thePath=Path.GetFileName(dir);
            // thePath="3xFish_Cube.001";
            this.ImportAllFromAnimation(importLocation, thePath);
            var SaveOK = EditorSceneManager.SaveScene(EditorSceneManager.GetActiveScene(), "Assets/Scenes/"+thePath+".unity");
        }
    }


    private void ImportAllFromAnimation(string importLocation, string animationName)
    {
        string dirPath = importLocation+"/"+animationName;
        string[] dirs = Directory.GetDirectories(dirPath, "*", SearchOption.TopDirectoryOnly);

        float startingOffset = ((-1*dirs.Length-1)/2);
        int i = 0;

        foreach (string dir in dirs) {
            var dirName = new DirectoryInfo(dir).Name;
            this.Import4DShape(importLocation, animationName, dirName, (startingOffset+(float)i));
            i=i+1;
        }
    }

    // Use the TextureImporter to modify the texture to the correct settings
    private void Import4DShape(string importLocation, string animationName, string exact4dShape, float offset)
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


        string fullPath = importLocation+"/"+animationName+"/"+exact4dShape;
        Debug.Log("Path is: "+fullPath);
        string[] objectFiles = Directory.GetFiles(fullPath);
        EditorApplication.ExecuteMenuItem("GameObject/Create Other/MegaCache/OBJ Cache");
        GameObject newMegaCache = GameObject.Find("Mega Cache Obj");

        newMegaCache.name=exact4dShape;
        Vector3 megaCacheObjectVector=newMegaCache.transform.position;
        newMegaCache.transform.position=new Vector3(offset, 1.1f, offset);

        Vector3 megaCacheObjectScale=newMegaCache.transform.localScale;
        newMegaCache.transform.localScale=new Vector3(0.04f, 0.04f, 0.04f);

        Debug.Log(megaCacheObjectVector.x);

        Debug.Log(GameObject.Find(exact4dShape).transform.position);

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
