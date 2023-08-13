#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;
using System.Collections.Generic;
using UnityEditor.SceneManagement;
using UnityEngine.SceneManagement;
using System.IO;
using System.Linq;

public class ImportLumped : EditorWindow 
{

    private Dictionary<GameObject, List<string>> cubeFilenames = new Dictionary<GameObject, List<string>>();


    // Top-level directory to import
    private string topLevelDirectory = "C:/Users/DanDo/OneDrive/Desktop/FinalFrames/lumpedansibleexports";

    // Original scene path
    private string entranceTemplateScenePath = "Assets/Scenes/templates/TemplateEntrance.unity";

    // Cube line start position
    private Vector3 cubeStartPosition = new Vector3(0, 0, 5);
    private float cubeSpacing = 4.0f;

    // List to hold created materials
    private List<(Material, Material)> createdMaterials = new List<(Material, Material)>();

    // Creates a toolbar, when selected implicitly calls ShowWindow()
    [MenuItem("DansCustomTools/Import New lumped 4d Shapes into museum")]
    private static void ShowWindow()
    {
        // Creates the main window, implicitly takes the content from OnGUI()
        var window = GetWindow<ImportLumped>();
        window.titleContent = new GUIContent("Import New lumped 4d Shapes into museum");
        window.Show();
    }


    private void OnGUI()
    {

        topLevelDirectory = EditorGUILayout.TextField("Top-level Import Directory", topLevelDirectory);

        string[] subdirectories = Directory.GetDirectories(topLevelDirectory);

        if (GUILayout.Button("Import Everything into museum"))
        {
            foreach (string subdir in subdirectories)
            {

                string[] files = Directory.GetFiles(subdir, "*.obj");

                foreach (string file in files)
                {
                    // Get the filename without extension
                    string filename = Path.GetFileNameWithoutExtension(file);

                    // Split the filename by underscore
                    string[] filenameParts = filename.Split('_');

                    // Construct the first and second subdirectory names
                    string firstSubDirName = filenameParts[0];

                    string secondSubDirName = string.Join("_", filenameParts.Take(filenameParts.Length - 1));

                    // Create the first subdirectory path
                    string firstSubDirPath = Path.Combine(topLevelDirectory, subdir, firstSubDirName);

                    // Create the first subdirectory if it doesn't exist
                    if (!Directory.Exists(firstSubDirPath))
                    {
                        Directory.CreateDirectory(firstSubDirPath);
                    }

                    // Create the new file path
                    string newFilePath = Path.Combine(firstSubDirPath, Path.GetFileName(file));

                    // Check if the file already exists at the new location
                    if (File.Exists(newFilePath))
                    {
                        // Delete the existing file
                        File.Delete(newFilePath);
                    }
                    else
                    {
                        // Move the file into the second subdirectory
                        File.Move(file, newFilePath);
                    }
                }
            }


            // Get all import locations
            Dictionary<string, List<string>> importLocations = new Dictionary<string, List<string>>();
            foreach (var dir in Directory.GetDirectories(topLevelDirectory))
            {
                string parentDir = new DirectoryInfo(dir).Name;
                importLocations[parentDir] = new List<string>(Directory.GetDirectories(dir, "*", SearchOption.TopDirectoryOnly));
            }

            
            // Create the cubes in the newly named scene
            var totalDirectories = importLocations.Count;


            // Create the materials before the scene creation
            CreateMaterials(CountDirectories(Directory.GetDirectories(topLevelDirectory).ToList()));


            string newEntranceScenePath = "Assets/Scenes/-CreatedFullMuseum.unity";


            if (!File.Exists(newEntranceScenePath))
            {
                EditorSceneManager.OpenScene(entranceTemplateScenePath, OpenSceneMode.Single);
                var entranceSaveOK = EditorSceneManager.SaveScene(EditorSceneManager.GetActiveScene(), newEntranceScenePath);
            }
            else
            {
                Debug.Log("Loading Museum");
            }

            // Clear the list of build scenes
            List<EditorBuildSettingsScene> buildScenes = new List<EditorBuildSettingsScene>();

            // Add new entrance scene as the first scene
            buildScenes.Add(new EditorBuildSettingsScene(newEntranceScenePath, true));

            // Set the build settings scenes to the new list of scenes
            EditorBuildSettings.scenes = buildScenes.ToArray();

            // Open the scene as the museum if it isn't open
            if (SceneManager.GetActiveScene().name != "-CreatedFullMuseum")
            {
                EditorSceneManager.OpenScene("Assets/Scenes/-CreatedFullMuseum.unity", OpenSceneMode.Single);
            }

            int line = 0;
            int globalIndex = 0;
            foreach (var parentDir in importLocations)
            {

                var materials = createdMaterials[globalIndex];

                int totalSubDirectories = parentDir.Value.Count;

                GameObject cube = GameObject.CreatePrimitive(PrimitiveType.Cube);
                cube.name = parentDir.Key;

                Vector3 cubePosition = cubeStartPosition + new Vector3(cubeSpacing, 0, line * cubeSpacing);
                cube.transform.position = cubePosition;
                cube.transform.localScale = new Vector3(1.2f, 1.2f, 1.2f); 
                cube.GetComponent<Renderer>().material = materials.Item1;

                ChangeCubeMaterial ccm;

                ccm = cube.AddComponent<ChangeCubeMaterial>();

                ccm.newMaterial = materials.Item2;
                ccm.originalMaterial = materials.Item1;
                ccm.mainCamera = GameObject.Find("Main Camera");

                // Split the filename and assign it to the cube
                ccm.filenameParts = parentDir.Key.Split('_').ToList();

                for (int i = 0; i < totalSubDirectories; i++)
                {

                    materials = createdMaterials[globalIndex];

                    string fullPath = parentDir.Value[i];
                    Debug.Log(fullPath);

                    Debug.Log("Ind files:");
                    string[] objectFiles = Directory.GetFiles(fullPath);

                    foreach (string CheckDafile in objectFiles)
                    {
                        Debug.Log(CheckDafile);
                    }

                    var dir4dName = new DirectoryInfo(parentDir.Value[i]).Name;
                    
                    EditorApplication.ExecuteMenuItem("GameObject/Create Other/MegaCache/OBJ Cache");
                    GameObject fourDobj = GameObject.Find("Mega Cache Obj");
                    fourDobj.name="4D_Obj_"+dir4dName;
                    // }

                    fourDobj.transform.position=new Vector3(0.0f, 1.5f, 0.0f);
                    fourDobj.transform.position = fourDobj.transform.position + cubePosition;

                    MegaCacheOffset megaCacheOffset = fourDobj.GetComponent<MegaCacheOffset>();
                    if (megaCacheOffset != null)
                    {
                        fourDobj.transform.position += megaCacheOffset.offset;
                    }
                    else
                    {
                        megaCacheOffset = fourDobj.AddComponent<MegaCacheOffset>();
                    }


                    Vector3 megaCacheObjectScale=fourDobj.transform.localScale;
                    fourDobj.transform.localScale=new Vector3(0.12f, 0.12f, 0.12f);

                    var megaCacheComponent=fourDobj.GetComponent<MegaCacheOBJ>();
                    
                    megaCacheComponent.fps=10.0f;
                    megaCacheComponent.animate=false;

                    // if (needsCreation)
                    // {
                    int fCount = Directory.GetFiles(fullPath, "*", SearchOption.TopDirectoryOnly).Length;
                    megaCacheComponent.lastframe=(fCount-1);

                    string file = objectFiles[0];

                    if ( file != null && file.Length > 1 )
                    {
                        megaCacheComponent.lastpath = file;
                        LoadOBJ(megaCacheComponent, file, megaCacheComponent.firstframe, megaCacheComponent.lastframe, megaCacheComponent.skip);
                    }
                    megaCacheComponent.Start();
                    // }

                    ccm.connectedMegaCaches.Add(fourDobj);

                    MeshRenderer my_mr=(MeshRenderer)fourDobj.GetComponent<MeshRenderer>();

                    var mat = materials.Item1;

                    my_mr.sharedMaterial = mat;

                    Material[] sharedMaterialsCopy = new Material[2];
                    sharedMaterialsCopy[0] = mat;
                    sharedMaterialsCopy[1] = mat;
                    my_mr.sharedMaterials = sharedMaterialsCopy;

                    globalIndex++;
                }
                line++;
            }
        }

        if (GUILayout.Button("Close"))
        {
            this.Close();
        }
    }



    private void CreateMaterials(int count)
    {

        string materialsDirectoryPath = "Assets/Materials";
        // Get all material files from the materials directory
        string[] materials = Directory.GetFiles(materialsDirectoryPath, "*.mat");

        // Iterate through each material file
        foreach (string material in materials)
        {
            // Delete the asset
            AssetDatabase.DeleteAsset(material);
        }
        for (int i = 0; i < count; i++)
        {

            // Create a new material with a random color
            Material randomMaterial = new Material(Shader.Find("Standard"));
            randomMaterial.color = new Color(Random.value, Random.value, Random.value);

            // Save the material as an asset
            AssetDatabase.CreateAsset(randomMaterial, $"Assets/Materials/randomMaterial{i}.mat");

            // Create a lighter variant of the same color
            Color lighterColor = new Color(Mathf.Min(randomMaterial.color.r + 0.4f, 1.0f),
                                        Mathf.Min(randomMaterial.color.g + 0.4f, 1.0f),
                                        Mathf.Min(randomMaterial.color.b + 0.4f, 1.0f));
            Material lighterMaterial = new Material(Shader.Find("Standard"));
            lighterMaterial.color = lighterColor;

            // Save the lighter material as an asset
            AssetDatabase.CreateAsset(lighterMaterial, $"Assets/Materials/lighterMaterial{i}.mat");

            // Add the pair of materials to the list
            createdMaterials.Add((randomMaterial, lighterMaterial));
        }
    }




   // Counts total number of subdirectories in all import locations
    private int CountDirectories(List<string> locations)
    {
        int count = 0;
        foreach (string location in locations)
        {
            count += Directory.GetDirectories(location, "*", SearchOption.AllDirectories).Length;
        }
        return count;
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
        }

		for ( int i = first; i <= last; i += step )
		{
			float a = (float)(i + 1 - first) / (last - first);
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
#endif