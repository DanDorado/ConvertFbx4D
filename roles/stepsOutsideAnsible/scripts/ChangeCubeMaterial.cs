using UnityEngine;
using System.Collections.Generic;
using TMPro;
using UnityEngine.UI;
using System.Text;
using UnityEngine.EventSystems;


public class ChangeCubeMaterial : MonoBehaviour
{

    [SerializeField]
    private float sliderValue;

    [SerializeField]
    private float sliderSpeedValue;

    public Material newMaterial;
    public Material originalMaterial;
    public GameObject mainCamera;
    public TextMeshProUGUI textDisplay;
    public List<GameObject> connectedMegaCaches = new List<GameObject>();
    public List<string> filenameParts;
    private MeshRenderer meshRenderer;
    private Image panelImage;
    private RectTransform panelRectTransform;

    private Slider slider;

    private Slider sliderSpeed;

    public TextMeshProUGUI sliderTextDisplay;

    public TextMeshProUGUI sliderSpeedTextDisplay;

    private Image sliderBackgroundImage;
    private Image sliderHandleImage;
    private RectTransform sliderRectTransform;

    private Image sliderSpeedBackgroundImage;
    private Image sliderSpeedHandleImage;
    private RectTransform sliderSpeedRectTransform;

    private Image toggleBackgroundImage;
    private Image toggleCheckmarkImage;


    // Defining constants here
    private const float PANEL_ALPHA = 0.5f;
    private const float SLIDER_BG_ALPHA = 1f;
    private const float SLIDER_HANDLE_ALPHA = 1f;
    private const float DISTANCE_THRESHOLD = 3.5f;
    private const float PADDING = 10;
    private const float SLIDER_TEXT_ALPHA = 1f;

    private float sliderIncrementRate = 5f;


    // Define constants for the size of the slider
    private const float SLIDER_WIDTH = 1000;

    [SerializeField]
    private bool incrementBool = true;


    private Toggle toggle;
    private bool isPlayerInteraction;




    private void Start()
    {

        // Cache the MeshRenderer component
        meshRenderer = GetComponent<MeshRenderer>();

        // Create a Canvas GameObject
        GameObject canvasObject = new GameObject("Canvas");
        Canvas canvas = canvasObject.AddComponent<Canvas>();
        canvas.renderMode = RenderMode.WorldSpace;  // Use world space, not screen space
        canvasObject.AddComponent<CanvasScaler>();
        canvasObject.AddComponent<GraphicRaycaster>();

        // Position the canvas near the cube (you may need to adjust these values)
        canvasObject.transform.position = transform.position + new Vector3(0, 0.9f, -1.3f);

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
        canvasObject.transform.localScale = new Vector3(0.0006f, 0.0006f, 0.0006f);  // Adjust as needed
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
        slider = sliderObject.AddComponent<Slider>();

        // Create a Slider GameObject for speed
        GameObject sliderSpeedObject = new GameObject("SliderSpeed");
        sliderSpeed = sliderSpeedObject.AddComponent<Slider>();

        // Create a Background Image for the slider
        GameObject sliderBackground = new GameObject("SliderBackground");
        sliderBackground.transform.SetParent(sliderObject.transform, false);
        sliderBackgroundImage = sliderBackground.AddComponent<Image>();
        sliderBackgroundImage.color = new Color(0.5f, 0.5f, 0.5f, 0.5f);

        // Create a Background Image for the Speed slider
        GameObject sliderSpeedBackground = new GameObject("SliderSpeedBackground");
        sliderSpeedBackground.transform.SetParent(sliderSpeedObject.transform, false);
        sliderSpeedBackgroundImage = sliderSpeedBackground.AddComponent<Image>();
        sliderSpeedBackgroundImage.color = new Color(0.5f, 0.5f, 0.5f, 0.5f);

        // Create a Handle for the slider
        GameObject sliderHandle = new GameObject("SliderHandle");
        sliderHandle.transform.SetParent(sliderObject.transform, false);
        sliderHandleImage = sliderHandle.AddComponent<Image>();
        sliderHandleImage.color = Color.white;  // Set the color as needed

        // Create a Handle for the Speed slider
        GameObject sliderSpeedHandle = new GameObject("SliderSpeedHandle");
        sliderSpeedHandle.transform.SetParent(sliderSpeedObject.transform, false);
        sliderSpeedHandleImage = sliderSpeedHandle.AddComponent<Image>();
        sliderSpeedHandleImage.color = Color.white;  // Set the color as needed

        // Assign the RectTransform of the Handle as the RectTransform of the slider
        slider.handleRect = sliderHandle.GetComponent<RectTransform>();
        slider.handleRect.sizeDelta = new Vector2(10, 10);  // Adjust as needed
        slider.handleRect.anchorMin = new Vector2(0, 0.5f);
        slider.handleRect.anchorMax = new Vector2(1, 0.5f);
        slider.handleRect.pivot = new Vector2(0.5f, 0.5f);
        slider.handleRect.anchoredPosition = new Vector2(0, 0);

        // Assign the RectTransform of the Handle as the RectTransform of the slider
        sliderSpeed.handleRect = sliderSpeedHandle.GetComponent<RectTransform>();
        sliderSpeed.handleRect.sizeDelta = new Vector2(10, 10);  // Adjust as needed
        sliderSpeed.handleRect.anchorMin = new Vector2(0, 0.5f);
        sliderSpeed.handleRect.anchorMax = new Vector2(1, 0.5f);
        sliderSpeed.handleRect.pivot = new Vector2(0.5f, 0.5f);
        sliderSpeed.handleRect.anchoredPosition = new Vector2(0, 0);


        RectTransform sliderHandleRect = sliderHandle.GetComponent<RectTransform>();
        sliderHandleRect.sizeDelta = new Vector2(5, 100);  // Adjust as needed

        RectTransform sliderSpeedHandleRect = sliderSpeedHandle.GetComponent<RectTransform>();
        sliderSpeedHandleRect.sizeDelta = new Vector2(5, 100);  // Adjust as needed

        // Set the slider properties
        slider.wholeNumbers = true;  // Use whole numbers for the slider values
        slider.minValue = 0f;  // Set the minimum value of the slider
        slider.maxValue = 250f;  // Set the maximum value of the slider
        slider.value = 0f;  // Set the initial value of the slider

        // Set the slider Speed properties
        sliderSpeed.wholeNumbers = true;  // Use whole numbers for the slider values
        sliderSpeed.minValue = 0f;  // Set the minimum value of the slider
        sliderSpeed.maxValue = 100f;  // Set the maximum value of the slider
        sliderSpeed.value = 0f;  // Set the initial value of the slider

        slider.direction = Slider.Direction.LeftToRight; // Ensure the direction is left to right

        sliderSpeed.direction = Slider.Direction.LeftToRight; // Ensure the Speed direction is left to right

        // Make the Slider a child of the Background GameObject
        sliderObject.transform.SetParent(panelObject.transform, false);

        // Set RectTransform to position the Slider
        sliderRectTransform = sliderObject.GetComponent<RectTransform>();
        sliderRectTransform.anchorMin = new Vector2(0.5f, 0.5f);
        sliderRectTransform.anchorMax = new Vector2(0.5f, 0.5f);
        sliderRectTransform.pivot = new Vector2(0.5f, 0.5f);
        sliderRectTransform.anchoredPosition3D = new Vector3(0, 0, 0);
        sliderRectTransform.anchoredPosition = new Vector2(0, 450);
        sliderRectTransform.sizeDelta = new Vector2(SLIDER_WIDTH, 5);

        // Make the Slider a child of the Background GameObject
        sliderSpeedObject.transform.SetParent(panelObject.transform, false);

        // Set RectTransform to position the Slider
        sliderSpeedRectTransform = sliderSpeedObject.GetComponent<RectTransform>();
        sliderSpeedRectTransform.anchorMin = new Vector2(0.5f, 0.5f);
        sliderSpeedRectTransform.anchorMax = new Vector2(0.5f, 0.5f);
        sliderSpeedRectTransform.pivot = new Vector2(0.5f, 0.5f);
        sliderSpeedRectTransform.anchoredPosition3D = new Vector3(0, 0, 0);
        sliderSpeedRectTransform.anchoredPosition = new Vector2(0, 320);
        sliderSpeedRectTransform.sizeDelta = new Vector2(SLIDER_WIDTH, 5);

        // Assign the RectTransform of the Background Image as the RectTransform of the slider
        RectTransform sliderProgressBar = sliderBackground.GetComponent<RectTransform>();

        // Adjust the anchors, position, and size of the RectTransform
        sliderProgressBar.anchorMin = new Vector2(0, 0.5f);
        sliderProgressBar.anchorMax = new Vector2(1, 0.5f);
        sliderProgressBar.sizeDelta = new Vector2(0, sliderProgressBar.sizeDelta.y);
        sliderProgressBar.anchoredPosition = new Vector2(0, 0);

        // Assign the RectTransform of the Background Image as the RectTransform of the slider
        RectTransform sliderSpeedProgressBar = sliderSpeedBackground.GetComponent<RectTransform>();

        // Adjust the anchors, position, and size of the RectTransform
        sliderSpeedProgressBar.anchorMin = new Vector2(0, 0.5f);
        sliderSpeedProgressBar.anchorMax = new Vector2(1, 0.5f);
        sliderSpeedProgressBar.sizeDelta = new Vector2(0, sliderSpeedProgressBar.sizeDelta.y);
        sliderSpeedProgressBar.anchoredPosition = new Vector2(0, 0);

        
        // Assign a callback for when the slider value changes
        slider.onValueChanged.AddListener(delegate { OnSliderValueChanged(slider.value); });

        // Assign a callback for when the slider value changes
        sliderSpeed.onValueChanged.AddListener(delegate { OnSliderSpeedValueChanged(sliderSpeed.value); });

        // Create a TextMeshProUGUI GameObject for the slider
        GameObject sliderTextObject = new GameObject("SliderText");
        sliderTextDisplay = sliderTextObject.AddComponent<TextMeshProUGUI>();

        // Create a TextMeshProUGUI GameObject for the slider
        GameObject sliderSpeedTextObject = new GameObject("SliderSpeedText");
        sliderSpeedTextDisplay = sliderSpeedTextObject.AddComponent<TextMeshProUGUI>();

        // Set the text properties
        sliderTextDisplay.font = Resources.Load<TMP_FontAsset>("Fonts & Materials/ARIAL SDF");  // Use the path of your preferred font asset
        sliderTextDisplay.text = "50";  // Put some test text in there to start with
        sliderTextDisplay.fontSize = 40;  // Increase font size because the text is now in world space
        sliderTextDisplay.color = Color.black;  // Set the color as needed

        // Set the text properties
        sliderSpeedTextDisplay.font = Resources.Load<TMP_FontAsset>("Fonts & Materials/ARIAL SDF");  // Use the path of your preferred font asset
        sliderSpeedTextDisplay.text = "Hyperplane Speed: 50";  // Put some test text in there to start with
        sliderSpeedTextDisplay.fontSize = 40;  // Increase font size because the text is now in world space
        sliderSpeedTextDisplay.color = Color.black;  // Set the color as needed

        // Make the TextMeshProUGUI element a child of the Slider GameObject
        sliderTextObject.transform.SetParent(sliderObject.transform, false);

        // Make the TextMeshProUGUI element a child of the Slider GameObject
        sliderSpeedTextObject.transform.SetParent(sliderSpeedObject.transform, false);

        // Set RectTransform to fill the Slider
        RectTransform sliderTextRectTransform = sliderTextObject.GetComponent<RectTransform>();
        sliderTextRectTransform.anchorMin = new Vector2(0.5f, 0.5f);
        sliderTextRectTransform.anchorMax = new Vector2(0.5f, 0.5f);
        sliderTextRectTransform.pivot = new Vector2(0.5f, 0.5f);
        sliderTextRectTransform.anchoredPosition3D = new Vector3(0, 0, 0);
        sliderTextRectTransform.anchoredPosition = new Vector2(0, 0);
        sliderTextRectTransform.sizeDelta = new Vector2(50, 50);  // Adjust as needed
        sliderTextDisplay.alignment = TextAlignmentOptions.Center;
        sliderTextDisplay.enableWordWrapping = false;

        slider = sliderObject.GetComponent<Slider>();

        // Set RectTransform to fill the Slider
        RectTransform sliderSpeedTextRectTransform = sliderSpeedTextObject.GetComponent<RectTransform>();
        sliderSpeedTextRectTransform.anchorMin = new Vector2(0.5f, 0.5f);
        sliderSpeedTextRectTransform.anchorMax = new Vector2(0.5f, 0.5f);
        sliderSpeedTextRectTransform.pivot = new Vector2(0.5f, 0.5f);
        sliderSpeedTextRectTransform.anchoredPosition3D = new Vector3(0, 0, 0);
        sliderSpeedTextRectTransform.anchoredPosition = new Vector2(0, 0);
        sliderSpeedTextRectTransform.sizeDelta = new Vector2(50, 50);  // Adjust as needed
        sliderSpeedTextDisplay.alignment = TextAlignmentOptions.Center;
        sliderSpeedTextDisplay.enableWordWrapping = false;

        sliderSpeed = sliderSpeedObject.GetComponent<Slider>();


        // Create a Toggle GameObject
        GameObject toggleObject = new GameObject("Toggle");
        toggle = toggleObject.AddComponent<Toggle>();

        // Create a Background Image for the Toggle
        GameObject toggleBackground = new GameObject("ToggleBackground");
        toggleBackground.transform.SetParent(toggleObject.transform, false);
        toggleBackgroundImage = toggleBackground.AddComponent<Image>();
        toggleBackgroundImage.color = new Color(144f/255f, 238f/255f, 144f/255f, 1f);


        // Create a Checkmark for the Toggle
        GameObject toggleCheckmark = new GameObject("ToggleCheckmark");
        toggleCheckmark.transform.SetParent(toggleBackground.transform, false);
        toggleCheckmarkImage = toggleCheckmark.AddComponent<Image>();
        toggleCheckmarkImage.color = new Color(238f/255f, 144f/255f, 144f/255f, 1f);

        // Assign the RectTransform of the Checkmark as the RectTransform of the Toggle
        toggle.graphic = toggleCheckmarkImage;
        toggle.targetGraphic = toggleBackgroundImage;

        // Set the Toggle properties
        toggle.isOn = false;  // Set the initial state of the Toggle

        // Make the Toggle a child of the Background GameObject
        toggleObject.transform.SetParent(panelObject.transform, false);

        // Set RectTransform to position the Toggle
        RectTransform toggleRectTransform = toggleObject.GetComponent<RectTransform>();
        toggleRectTransform.anchorMin = new Vector2(0.5f, 0.5f);
        toggleRectTransform.anchorMax = new Vector2(0.5f, 0.5f);
        toggleRectTransform.pivot = new Vector2(0.5f, 0.5f);
        toggleRectTransform.anchoredPosition3D = new Vector3(0, 0, 0);
        toggleRectTransform.anchoredPosition = new Vector2(-570, 450);  // adjust as needed
        toggleRectTransform.sizeDelta = new Vector2(100, 100);  // adjust as needed

        // Assign a callback for when the Toggle value changes
        toggle.onValueChanged.AddListener(delegate { OnToggleValueChanged(toggle.isOn); });

    }


    private void OnToggleValueChanged(bool value)
    {
        incrementBool = !value;
    }


    private void OnSliderValueChanged(float value)
    {
        if (isPlayerInteraction)
        {
            toggle.isOn = true;
        }
        sliderValue = value;

        int frameValue = Mathf.RoundToInt(value);

        foreach (GameObject connectedMegaCache in connectedMegaCaches)
        {
            var megaCacheComponent=connectedMegaCache.GetComponent<MegaCacheOBJ>();
            megaCacheComponent.frame = frameValue;
        }


        sliderTextDisplay.text = "Frame: " + (frameValue + 1).ToString("0");
    }

    private void OnSliderSpeedValueChanged(float value)
    {
        sliderSpeedValue = value;
        sliderIncrementRate = sliderSpeedValue;
        int frameValue = Mathf.RoundToInt(value);
        sliderSpeedTextDisplay.text = "Hyperplane Speed " + (frameValue).ToString("0");
    }


    private void Update()
    {

        float distance = Vector3.Distance(mainCamera.transform.position, transform.position);
        StringBuilder displayText = new StringBuilder();
        string finalText = "\n\n<b><color=orange>Press '</color><color=white>k</color><color=red>' to select this shape</b></color>";

        if (distance <= DISTANCE_THRESHOLD)
        {
            meshRenderer.material = newMaterial;
            SetAlphaOfUIElements(PANEL_ALPHA, SLIDER_BG_ALPHA, SLIDER_HANDLE_ALPHA, SLIDER_TEXT_ALPHA, 1f, 1f);

            string hyperplaneName = "";

            if(filenameParts.Count >= 3)
            {
                if (filenameParts[2] == "KL")
                {
                    hyperplaneName = filenameParts[6];
                }
                else if (filenameParts[2] == "BBP")
                {
                    hyperplaneName = filenameParts[4];
                }
                else if (filenameParts[2] == "HP")
                {
                    hyperplaneName = filenameParts[4];
                }
            }
            else
            {
                hyperplaneName = filenameParts[0];
            }

            string hyperplaneVector = "";

            switch(hyperplaneName) {
                case "randomHyperplane1":
                    hyperplaneVector = "x:    0.1      y:    2.2      z:    -1.4      w:    -14";
                    break;
                case "Hyperplane1":
                    hyperplaneVector = "x:    0      y:    1      z:    0      w:    0";
                    break;
                case "Hyperplane2":
                    hyperplaneVector = "x:    1      y:    0      z:    0      w:    0";
                    break;
                case "Hyperplane0":
                    hyperplaneVector = "x:    0      y:    0      z:    0      w:    1";
                    break;
                case "Hyperplane3":
                    hyperplaneVector = "x:    0      y:    0      z:    1      w:    0";
                    break;
                case "HyperPlaneCloseWZ":
                    hyperplaneVector = "x:    0      y:    0      z:    0.5      w:    1";
                    break;
                case "HyperPlaneCloseWY":
                    hyperplaneVector = "x:    0      y:    0.5      z:    0      w:    1";
                    break;
                case "HyperPlaneCloseWX":
                    hyperplaneVector = "x:    0.5      y:    0      z:    0      w:    1";
                    break;
                case "randomHyperplane2":
                    hyperplaneVector = "x:    1.2      y:    0.2      z:    12.4      w:    -3.44";
                    break;
                case "randomHyperplane3":
                    hyperplaneVector = "FirstString was selected.";
                    break;
                default:
                    hyperplaneVector = "Unknown Hyperplane not in records";
                    break;
            }
                
                
                
              



            if(filenameParts.Count >= 3)
            {
                if (filenameParts[2] == "KL")
                {
                    displayText.Append("Animation: <b><color=yellow>").Append(filenameParts[0]).Append("</b></color>\nNumber of animation loops: <b><color=yellow>").Append(filenameParts[1]).Append("</b></color>\nType of 4d image: <b><color=yellow>Hyperloop through spacetime</b></color>\nAxis rotated into time (x=1,y=2,z=0): <b><color=yellow>").Append(filenameParts[3]).Append("</b></color>\nNumber of rotations using the two remaining spatial dimensions: <b><color=yellow>").Append(filenameParts[5]).Append("</b></color>\nDistance from the centre of the animation to the centre of the spacetime loop: <b><color=yellow>").Append(filenameParts[4]).Append("</b></color>\nName of Hyperplane: <b><color=yellow>").Append(filenameParts[6]).Append("</b></color>\nHyperplane Vector: <b><color=yellow>").Append(hyperplaneVector).Append("</b></color>\nHyperplane Slices calculated: <b><color=yellow>").Append(filenameParts[7]).Append("</b></color>");
                    displayText.Append(finalText);
                }
                else if (filenameParts[2] == "BBP")
                {
                    displayText.Append("Animation: <b><color=yellow>").Append(filenameParts[0]).Append("</b></color>\nNumber of animation loops: <b><color=yellow>").Append(filenameParts[1]).Append("</b></color>\nType of 4d image: <b><color=yellow>Block Bounded Prism</b></color>\nConversion rate between space and time: <b><color=yellow>").Append(filenameParts[3]).Append("</b></color>\nName of Hyperplane: <b><color=yellow>").Append(filenameParts[4]).Append("</b></color>\nHyperplane Vector: <b><color=yellow>").Append(hyperplaneVector).Append("</b></color>\nHyperplane Slices calculated: <b><color=yellow>").Append(filenameParts[5]).Append("</b></color>");
                    displayText.Append(finalText);
                }
                else if (filenameParts[2] == "HP")
                {
                    displayText.Append("Animation: <b><color=yellow>").Append(filenameParts[0]).Append("</b></color>\nNumber of animation loops: <b><color=yellow>").Append(filenameParts[1]).Append("</b></color>\nType of 4d image: <b><color=yellow>Unbounded/Hollow Prism</b></color>\nConversion rate between space and time: <b><color=yellow>").Append(filenameParts[3]).Append("</b></color>\nName of Hyperplane: <b><color=yellow>").Append(filenameParts[4]).Append("</b></color>\nHyperplane Vector: <b><color=yellow>").Append(hyperplaneVector).Append("</b></color>\nHyperplane Slices calculated: <b><color=yellow>").Append(filenameParts[5]).Append("</b></color>");
                    displayText.Append(finalText);
                }
            }
            else
            {
                displayText.Append("Hypercube as seen with hyperplane intersection: <b><color=yellow>").Append(filenameParts[0]).Append("</b></color>\nHyperplane Vector: <b><color=yellow>").Append(hyperplaneVector);
            }

            textDisplay.text = displayText.ToString();

            // Rotate the text to face the camera
            textDisplay.transform.parent.transform.LookAt(mainCamera.transform);
            textDisplay.transform.parent.transform.Rotate(0, 180, 0);
        }
        else
        {
            meshRenderer.material = originalMaterial;
            textDisplay.text = "";
            SetAlphaOfUIElements(0f, 0f, 0f, 0f, 0f, 0f); // added 0f for sliderTextAlpha
        }

        // Adjust the panel size and slider position regardless of the distance condition
        Vector2 newSize = new Vector2(textDisplay.preferredWidth + PADDING, textDisplay.preferredHeight + PADDING);
        panelRectTransform.sizeDelta = newSize;

        if (incrementBool)
        {
            isPlayerInteraction = false;
            sliderValue = sliderValue + sliderIncrementRate * Time.deltaTime;
        }


        slider.value = sliderValue;

        // If the slider value has reached its maximum, reset it to its minimum
        if (sliderValue >= slider.maxValue)
        {
            sliderValue = slider.minValue;
        }

        isPlayerInteraction = true;
    }


    private void SetAlphaOfUIElements(float panelAlpha, float sliderAlpha, float sliderHandleAlpha, float sliderTextAlpha, float toggleBackgroundAlpha, float toggleCheckmarkAlpha)
    {
        Color panelColor = panelImage.color;
        panelColor.a = panelAlpha;
        panelImage.color = panelColor;

        Color sliderBackgroundColor = sliderBackgroundImage.color;
        sliderBackgroundColor.a = sliderAlpha;
        sliderBackgroundImage.color = sliderBackgroundColor;

        Color sliderHandleColor = sliderHandleImage.color;
        sliderHandleColor.a = sliderHandleAlpha;
        sliderHandleImage.color = sliderHandleColor;

        Color sliderTextColor = sliderTextDisplay.color;
        sliderTextColor.a = sliderTextAlpha;
        sliderTextDisplay.color = sliderTextColor;

        Color sliderSpeedBackgroundColor = sliderSpeedBackgroundImage.color;
        sliderSpeedBackgroundColor.a = sliderAlpha;
        sliderSpeedBackgroundImage.color = sliderSpeedBackgroundColor;

        Color sliderSpeedHandleColor = sliderSpeedHandleImage.color;
        sliderSpeedHandleColor.a = sliderHandleAlpha;
        sliderSpeedHandleImage.color = sliderSpeedHandleColor;

        Color sliderSpeedTextColor = sliderSpeedTextDisplay.color;
        sliderSpeedTextColor.a = sliderTextAlpha;
        sliderSpeedTextDisplay.color = sliderSpeedTextColor;
        
        // Setting the alpha for the toggle elements
        Color toggleBackgroundColor = toggleBackgroundImage.color;
        toggleBackgroundColor.a = toggleBackgroundAlpha;
        toggleBackgroundImage.color = toggleBackgroundColor;

        Color toggleCheckmarkColor = toggleCheckmarkImage.color;
        toggleCheckmarkColor.a = toggleCheckmarkAlpha;
        toggleCheckmarkImage.color = toggleCheckmarkColor;
    }
}
