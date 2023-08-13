#if UNITY_EDITOR
using UnityEditor;
using System.IO;
using System.Linq;
using UnityEditor.SceneManagement;

public class CleanUp
{
    [MenuItem("DansCustomTools/CleanUpAll")]
    public static void DeleteAllScenesAndMaterials()
    {
        // Define the directory paths
        string scenesDirectoryPath = "Assets/Scenes";
        string materialsDirectoryPath = "Assets/Materials";

        // Get all scene files from the scenes directory
        string[] scenes = Directory.GetFiles(scenesDirectoryPath, "*.unity");

        // Iterate through each scene file
        foreach (string scene in scenes)
        {
            // Delete the asset
            AssetDatabase.DeleteAsset(scene);
        }

        // Get all material files from the materials directory
        string[] materials = Directory.GetFiles(materialsDirectoryPath, "*.mat");

        // Iterate through each material file
        foreach (string material in materials)
        {
            // Delete the asset
            AssetDatabase.DeleteAsset(material);
        }

        // Clear all scenes from build settings
        EditorBuildSettings.scenes = new EditorBuildSettingsScene[0];

        // Refresh the AssetDatabase to update changes
        AssetDatabase.Refresh();
    }
}
#endif
