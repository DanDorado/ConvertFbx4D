#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;
using System.Collections.Generic;
using System.IO;
using System.Linq;

public class CountPotentialCreations : EditorWindow 
{
    private string topLevelDirectory = "C:/Users/DanDo/OneDrive/Desktop/FinalFrames/ansibleexports";

    [MenuItem("DansCustomTools/Count Potential Creations")]
    private static void ShowWindow()
    {
        var window = GetWindow<CountPotentialCreations>();
        window.titleContent = new GUIContent("Count Potential Creations");
        window.Show();
    }

    private void OnGUI()
    {
        topLevelDirectory = EditorGUILayout.TextField("Top-level Import Directory", topLevelDirectory);

        if (GUILayout.Button("Count"))
        {
            int newCubesCount = 0;
            int newScenesCount = 0;
            int existingCubesCount = 0;

            Dictionary<string, List<string>> importLocations = new Dictionary<string, List<string>>();
            foreach (var dir in Directory.GetDirectories(topLevelDirectory))
            {
                string parentDir = new DirectoryInfo(dir).Name;
                importLocations[parentDir] = new List<string>(Directory.GetDirectories(dir, "*", SearchOption.AllDirectories));
            }

            foreach (var parentDir in importLocations)
            {
                int totalSubDirectories = parentDir.Value.Count;

                for (int i = 0; i < totalSubDirectories; i++)
                {
                    string subdirName = new DirectoryInfo(parentDir.Value[i]).Name;

                    GameObject existingCube = GameObject.Find(subdirName);

                    if (existingCube == null)
                    {
                        newCubesCount++;
                    }
                    else
                    {
                        existingCubesCount++;
                    }

                    string newScenePath = $"Assets/Scenes/{subdirName}.unity";

                    if (!File.Exists(newScenePath))
                    {
                        newScenesCount++;
                    }
                }
            }

            Debug.Log($"New cubes to be created: {newCubesCount}");
            Debug.Log($"Existing cubes that would be affected: {existingCubesCount}");
            Debug.Log($"New scenes to be created: {newScenesCount}");
        }

        if (GUILayout.Button("Close"))
            this.Close();
    }
}
#endif
