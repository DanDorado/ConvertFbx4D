using System.IO;
using UnityEditor;
using UnityEngine;

public class CleanUpOBJ : EditorWindow
{
    // Top-level directory to import
    private string topLevelDirectory = "C:/Users/DanDo/OneDrive/Desktop/FinalFrames/ansibleexports";

    [MenuItem("DansCustomTools/Clean up OBJ files")]
    public static void ShowWindow()
    {
        GetWindow<CleanUpOBJ>("Clean up OBJ files");
    }

    void OnGUI()
    {
        GUILayout.Label("Base Settings", EditorStyles.boldLabel);
        topLevelDirectory = EditorGUILayout.TextField("Top Level Directory", topLevelDirectory);

        if (GUILayout.Button("Remove OBJs"))
        {
            DeleteObjFiles(topLevelDirectory);
        }
    }

    private void DeleteObjFiles(string path)
    {
        if (Directory.Exists(path))
        {
            foreach (var directory in Directory.GetDirectories(path))
            {
                string[] files = Directory.GetFiles(directory, "*.obj", SearchOption.AllDirectories);
                foreach (string file in files)
                {
                    File.Delete(file);
                    Debug.Log("Deleted: " + file);
                }
            }
            AssetDatabase.Refresh();
        }
        else
        {
            Debug.LogError("Directory not found: " + path);
        }
    }
}
