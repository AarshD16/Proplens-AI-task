# Proplens - Real Estate Analysis

Proplens is a Python-based GUI application that helps users analyze and compare real estate projects in a specific location. The application fetches details about nearby real estate projects, scrapes additional information from the web, and uses a language model to generate a detailed comparison of selected projects.

## Features

- **User Input**: Enter a place name to search for nearby real estate projects.
- **Geocoding**: Convert place names to geographic coordinates using Google Maps Geocoding API.
- **Nearby Places Search**: Find nearby real estate projects using Google Places API.
- **Data Collection**: Collect detailed information about each real estate project.
- **Web Scraping**: Supplement the data with additional information by scraping relevant websites.
- **LLM Integration**: Use a pre-trained language model to process and format data into a well-organized comparison table.
- **GUI Display**: View and compare the details of selected projects.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/proplens.git
    cd proplens
    ```

2. Set up a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Install PyTorch (for the language model):
    Follow the instructions at [PyTorch Installation](https://pytorch.org/get-started/locally/) to install the appropriate version for your system.

## Usage

1. Obtain your Google API key and set it as an environment variable:
    ```sh
    export GOOGLE_API_KEY='your_google_api_key'
    ```

2. Run the application:
    ```sh
    python main.py
    ```

3. Enter a place name in the GUI and click "Analyze" to fetch and display nearby real estate projects.

4. Select multiple projects from the list to view and compare their details.

## Code Explanation

### Approach

- **User Input**: Takes a place name as input from the user.
- **Geocoding**: Converts the place name to geographic coordinates using Google Maps Geocoding API.
- **Nearby Places Search**: Uses these coordinates to find nearby real estate projects using Google Places API.
- **Data Collection**: Collects detailed information about each real estate project.
- **Web Scraping**: Supplements the data with additional information by scraping relevant websites.
- **LLM Integration**: Uses a pre-trained language model to process and format this data into a well-organized comparison table.
- **GUI Display**: Displays the projects in a list where users can select multiple projects to view and compare their details.

### High-Level Code Flow

1. **Initialization**: Import libraries, initialize the Hugging Face model and tokenizer, set up the GUI layout.
2. **User Input**: User enters the place name and clicks "Analyze".
3. **Analyze Function**:
    - Retrieves geographic coordinates using `get_place_coordinates`.
    - Finds nearby real estate projects using `get_nearby_places`.
    - Gets additional details for each project using `get_place_details`.
    - Scrapes supplementary information using `web_scrape_information`.
    - Formats the collected information using the language model with `format_information_with_llm`.
4. **Display**: Displays the nearby projects in a listbox, shows details of selected projects, and compares selected projects using `compare_selected_projects`.

### Fine-Tuning the Model

To fine-tune the model, follow these steps:
1. **Data Collection**: Gather a dataset of real estate descriptions and comparisons.
2. **Preprocessing**: Clean and preprocess the data.
3. **Training**: Use the Hugging Face `transformers` library to fine-tune the model on the dataset.
4. **Validation**: Validate the model on a separate validation set.
5. **Deployment**: Integrate the fine-tuned model into the application.

### Cost Reduction Strategies

- **API Call Optimization**:
    - **Batch Requests**: Batch multiple API calls into a single request where possible.
    - **Caching**: Use Redis or another caching mechanism to store responses for frequently requested data.
- **Efficient Use of NLP**:
    - **Model Distillation**: Use a distilled version of the language model to reduce inference costs.
    - **Selective Summarization**: Only process new or changed data to avoid unnecessary computation.
- **Hybrid Approach**:
    - **Local Processing**: Perform initial data processing and filtering locally before making API calls.
    - **Edge Computing**: Use edge computing resources to offload some processing tasks.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## Contact

If you have any questions or feedback, please open an issue or reach out to `your.email@example.com`.

---

### Additional Questions

**Q: How do you handle errors when API calls fail?**
A: Error handling is implemented using try-except blocks. If an API call fails, the error is caught, and a relevant error message is displayed to the user.

**Q: What happens if the user enters an invalid place name?**
A: If the geocoding API cannot find the coordinates for the entered place, an error message is displayed to the user indicating that the location could not be found.

**Q: How are multiple projects compared in the application?**
A: The user can select multiple projects from the listbox. The details of these projects are then processed and formatted into a comparison table using the language model, which is displayed in the text widget.

**Q: What libraries are used for web scraping and why?**
A: The `requests` library is used to fetch web pages, and `BeautifulSoup` is used to parse and extract information from HTML content. These libraries are chosen for their ease of use and powerful capabilities in handling web scraping tasks.

**Q: How is the map generated and displayed to the user?**
A: The map is generated using the `folium` library. It marks the location of the target place and nearby real estate projects. The map is saved to an HTML file, which is then opened in the user's default web browser.

---

Enjoy using Proplens!
