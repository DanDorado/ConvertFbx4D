using UnityEngine;

[CreateAssetMenu(fileName = "HyperplaneAsset", menuName = "New Hyperplane Float Array Asset", order = 51)]
public class HyperplaneAsset : ScriptableObject
{
    public float[] floatArray = new float[4];
}
