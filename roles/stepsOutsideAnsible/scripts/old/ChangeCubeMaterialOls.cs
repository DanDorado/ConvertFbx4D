using UnityEngine;
using UnityEngine.SceneManagement;  // Required for scene management
using UnityEngine.XR;
using System.Collections.Generic;
using TMPro;
using UnityEngine.UI;


public class ChangeCubeMaterial : MonoBehaviour
{
    public Material newMaterial;  // The material the cube changes to when the player is within 2 units
    public Material originalMaterial;  // The original material of the cube
    public GameObject mainCamera;  // Reference to the Main Camera GameObject
    public int newSceneBuildIndex;  // The build index of the new scene to load

    private Image sliderBackgroundImage;
    private Image sliderHandleImage;


    public TextMeshProUGUI textDisplay;

    public GameObject connectedMegaCache;

    public List<string> filenameParts; 

    // Declare here
    private Image panelImage;
    private RectTransform panelRectTransform;


    private void Start()
    {
        // Create a Canvas GameObject
        GameObject canvasObject = new GameObject("Canvas");
        Canvas canvas = canvasObject.AddComponent<Canvas>();
        canvas.renderMode = RenderMode.WorldSpace;  // Use world space, not screen space
        canvasObject.AddComponent<CanvasScaler>();
        canvasObject.AddComponent<GraphicRaycaster>();

        // Adjust the scale of the Canvas
        canvasObject.transform.localScale = new Vector3(0.01f, 0.01f, 0.01f);  // Adjust as needed

        // Position the canvas near the cube (you may need to adjust these values)
        canvasObject.transform.position = transform.position + new Vector3(0, 0.9f, 0);

        // Create a TextMeshProUGUI GameObject
        GameObject textObject = new GameObject("Text");
        textDisplay = textObject.AddComponent<TextMeshProUGUI>();

        // Set the text properties
        textDisplay.font = Resources.Load<TMP_FontAsset>("Fonts & Materials/ARIAL SDF");  // Use the path of your preferred font asset
        textDisplay.text = "Test Text";  // Put some test text in there to start with
        textDisplay.fontSize = 40;  // Increase font size because the text is now in world space
        textDisplay.color = Color.black;
        

        // Make the TextMeshProUGUI element a child of the Canvas GameObject
        textObject.transform.SetParent(canvasObject.transform, false);

        // Set RectTransform to fill the parent Canvas
        RectTransform textRectTransform = textObject.GetComponent<RectTransform>();
        textRectTransform.anchorMin = new Vector2(0, 0);
        textRectTransform.anchorMax = new Vector2(1, 1);
        textRectTransform.pivot = new Vector2(0.5f, 0.5f);
        textRectTransform.anchoredPosition3D = new Vector3(0, 0, 0);
        textRectTransform.anchoredPosition = new Vector2(0, 0);
        canvasObject.transform.localScale = new Vector3(0.001f, 0.001f, 0.001f);  // Adjust as needed
        textRectTransform.sizeDelta = new Vector2(500, 200);  // Adjust as needed
        textDisplay.alignment = TextAlignmentOptions.Midline;
        textDisplay.enableWordWrapping = false;


        // Create a new UI Panel GameObject for the background
        GameObject panelObject = new GameObject("Background");
        panelObject.transform.SetParent(canvasObject.transform, false);
        panelRectTransform = panelObject.AddComponent<RectTransform>();
        panelRectTransform.anchorMin = new Vector2(0, 0);
        panelRectTransform.anchorMax = new Vector2(1, 1);
        panelRectTransform.pivot = new Vector2(0.5f, 0.5f);
        panelRectTransform.anchoredPosition3D = new Vector3(0, 0, 0);
        panelRectTransform.anchoredPosition = new Vector2(0, 0);
        panelRectTransform.sizeDelta = new Vector2(0, 0);  // Adjust as needed

        panelImage = panelObject.AddComponent<Image>();
        // Set the color and transparency of the image (this example sets it to a semi-transparent black)
        panelImage.color = new Color(0, 0, 0, 0.5f); // RGBA

        // Then assign the panel as the parent of the text.
        textObject.transform.SetParent(panelObject.transform, false);

        // Create a Slider GameObject
        GameObject sliderObject = new GameObject("Slider");
        Slider slider = sliderObject.AddComponent<Slider>();

        // Create a Background Image for the slider
        GameObject sliderBackground = new GameObject("SliderBackground");
        sliderBackground.transform.SetParent(sliderObject.transform, false);
        sliderBackgroundImage = sliderBackground.AddComponent<Image>();
        sliderBackgroundImage.color = Color.gray;  // Set the color as needed

        // Assign the RectTransform of the Background Image as the RectTransform of the slider
        slider.fillRect = sliderBackground.GetComponent<RectTransform>();

        // Create a Handle for the slider
        GameObject sliderHandle = new GameObject("SliderHandle");
        sliderHandle.transform.SetParent(sliderObject.transform, false);
        sliderHandleImage = sliderHandle.AddComponent<Image>();
        sliderHandleImage.color = Color.white;  // Set the color as needed

        // Assign the RectTransform of the Handle as the RectTransform of the slider
        slider.handleRect = sliderHandle.GetComponent<RectTransform>();


        var megaCacheComponent=connectedMegaCache.GetComponent<MegaCacheOBJ>();

        // Set the slider properties
        slider.minValue = 0f;  // Set the minimum value of the slider
        slider.maxValue = 100f;  // Set the maximum value of the slider
        slider.value = 50f;  // Set the initial value of the slider

        // Make the Slider a child of the Background GameObject
        sliderObject.transform.SetParent(panelObject.transform, false);

        


        // Set RectTransform to position the Slider
        RectTransform sliderRectTransform = sliderObject.GetComponent<RectTransform>();
        sliderRectTransform.anchorMin = new Vector2(0.5f, 0.5f);
        sliderRectTransform.anchorMax = new Vector2(0.5f, 0.5f);
        sliderRectTransform.pivot = new Vector2(0.5f, 0.5f);
        sliderRectTransform.anchoredPosition3D = new Vector3(0, -50, 0);
        sliderRectTransform.anchoredPosition = new Vector2(0, -50);
        sliderRectTransform.sizeDelta = new Vector2(250, 10);  // Adjust as needed
        
        // Assign a callback for when the slider value changes
        slider.onValueChanged.AddListener(delegate { OnSliderValueChanged(slider.value); });

    }

    private void OnSliderValueChanged(float value)
    {
        var megaCacheComponent=connectedMegaCache.GetComponent<MegaCacheOBJ>();
        megaCacheComponent.time = value;
    }


    private void Update()
    {
        float distance = Vector3.Distance(mainCamera.transform.position, transform.position);

        // If the player is within 2 units of the cube
        if (distance <= 2)
        {
            GetComponent<MeshRenderer>().material = newMaterial;

            // Display filename parts as text

            string displayText = "";

            string finalText = "\n\n<b><color=orange>Press '</color><color=white>k</color><color=red>' to select this shape</b></color>";
            if(filenameParts.Count >= 3)
            {
                if (filenameParts[2] == "KL")
                {
                    displayText = "Animation: <b><color=yellow>"+filenameParts[0]+"</b></color>\nNumber of animation loops: <b><color=yellow>"+filenameParts[1]+"</b></color>\nType of 4d image: <b><color=yellow>Hyperloop through spacetime</b></color>\nAxis rotated into time (x=1,y=2,z=0): <b><color=yellow>"+filenameParts[3]+"</b></color>\nNumber of rotations using the two remaining spatial dimensions: <b><color=yellow>"+filenameParts[5]+"</b></color>\nDistance from the centre of the animation to the centre of the spacetime loop: <b><color=yellow>"+filenameParts[4]+"</b></color>\nName of Hyperplane: <b><color=yellow>"+filenameParts[6]+"</b></color>\nHyperplane Slices calculated: <b><color=yellow>"+filenameParts[7]+"</b></color>";
                    displayText += finalText;
                }
                else if (filenameParts[2] == "BBP")
                {
                    displayText = "Animation: <b><color=yellow>"+filenameParts[0]+"</b></color>\nNumber of animation loops: <b><color=yellow>"+filenameParts[1]+"</b></color>\nType of 4d image: <b><color=yellow>Block Bounded Prism</b></color>\nConversion rate between space and time: <b><color=yellow>"+filenameParts[3]+"</b></color>\nName of Hyperplane: <b><color=yellow>"+filenameParts[4]+"</b></color>\nHyperplane Slices calculated: <b><color=yellow>"+filenameParts[5]+"</b></color>";
                    displayText += finalText;
                }
                else if (filenameParts[2] == "HP")
                {
                    displayText = "Animation: <b><color=yellow>" + filenameParts[0] + "</b></color>\nNumber of animation loops: <b><color=yellow>" + filenameParts[1] + "</b></color>\nType of 4d image: <b><color=yellow>Unbounded/Hollow Prism</b></color>\nConversion rate between space and time: <b><color=yellow>" + filenameParts[3] + "</b></color>\nName of Hyperplane: <b><color=yellow>" + filenameParts[4] + "</b></color>\nHyperplane Slices calculated: <b><color=yellow>" + filenameParts[5] + "</b></color>";
                    displayText += finalText;
                }
            }

            textDisplay.text = displayText;

            // Rotate the text to face the camera
            textDisplay.transform.parent.transform.LookAt(mainCamera.transform);
            textDisplay.transform.parent.transform.Rotate(0, 180, 0);
            


            // Check if the "A" button on the right controller is pressed
            InputDevice rightHandController;
            if (TryGetDeviceWithCharacteristics(InputDeviceCharacteristics.Right | InputDeviceCharacteristics.Controller, out rightHandController))
            {
                bool buttonPressed;
                if (rightHandController.TryGetFeatureValue(CommonUsages.primaryButton, out buttonPressed) && buttonPressed)
                {
                    // Load the new scene
                    SceneManager.LoadScene(newSceneBuildIndex);
                }
            }

            // Check if the 'k' key is pressed
            if (Input.GetKeyDown(KeyCode.K)) // KeyCode.K is for 'k' key
            {
                // Load the new scene
                SceneManager.LoadScene(newSceneBuildIndex);
            }

            Color newColor = panelImage.color;
            newColor.a = 0.5f;
            panelImage.color = newColor;

            Color sliderBackgroundColor = sliderBackgroundImage.color;
            sliderBackgroundColor.a = 1f;  // Adjust as needed
            sliderBackgroundImage.color = sliderBackgroundColor;

            Color sliderHandleColor = sliderHandleImage.color;
            sliderHandleColor.a = 1f;  // Adjust as needed
            sliderHandleImage.color = sliderHandleColor;
        }
        // If the player is more than 2 units away from the cube
        else
        {
            GetComponent<MeshRenderer>().material = originalMaterial;

            // Clear the displayed text
            textDisplay.text = "";

            Color newColor = panelImage.color;
            newColor.a = 0f;
            panelImage.color = newColor;

            Color sliderBackgroundColor = sliderBackgroundImage.color;
            sliderBackgroundColor.a = 0f;  // Adjust as needed
            sliderBackgroundImage.color = sliderBackgroundColor;

            Color sliderHandleColor = sliderHandleImage.color;
            sliderHandleColor.a = 0f;  // Adjust as needed
            sliderHandleImage.color = sliderHandleColor;

        }


        float padding = 10;
        Vector2 newSize = new Vector2(textDisplay.preferredWidth + padding, textDisplay.preferredHeight + padding);
        panelRectTransform.sizeDelta = newSize;
    }



    bool TryGetDeviceWithCharacteristics(InputDeviceCharacteristics inputDeviceCharacteristics, out InputDevice device)
    {
        List<InputDevice> devices = new List<InputDevice>();
        InputDevices.GetDevicesWithCharacteristics(inputDeviceCharacteristics, devices);
        if (devices.Count > 0)
        {
            device = devices[0];
            return true;
        }
        else
        {
            device = new InputDevice();
            return false;
        }
    }
}
