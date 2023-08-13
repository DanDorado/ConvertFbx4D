using UnityEngine;

public class ChangeCubeMaterial : MonoBehaviour
{
    public Material newMaterial;  // The material the cube changes to when the player is within 2 units
    public Material originalMaterial;  // The original material of the cube
    public GameObject mainCamera;  // Reference to the Main Camera GameObject

    private void Update()
    {
        float distance = Vector3.Distance(mainCamera.transform.position, transform.position);
        Debug.Log("Distance to camera: " + distance);

        // If the player is within 2 units of the cube, change the cube's material to newMaterial
        if (distance <= 2)
        {
            GetComponent<MeshRenderer>().material = newMaterial;
        }
        // If the player is more than 2 units away from the cube, change the cube's material back to originalMaterial
        else
        {
            GetComponent<MeshRenderer>().material = originalMaterial;
        }
    }
}
