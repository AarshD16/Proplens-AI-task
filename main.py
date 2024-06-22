import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext
import requests
from bs4 import BeautifulSoup
import folium
from io import BytesIO
import tempfile
import os
import webbrowser
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# Set your API keys
GOOGLE_API_KEY = 'YOUR API KEY'

# Initialize the Hugging Face model and tokenizer
model_name = "google/flan-t5-small"  # You can choose a different model here
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
summarization_pipeline = pipeline("summarization", model=model, tokenizer=tokenizer)


def get_place_coordinates(place):
    try:
        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={place}&key={GOOGLE_API_KEY}'
        response = requests.get(url)
        results = response.json().get('results', [])
        if not results:
            return None, None
        location = results[0]['geometry']['location']
        return location['lat'], location['lng']
    except Exception as e:
        print(f"Error getting place coordinates: {e}")
        return None, None


def get_nearby_places(lat, lng, radius=2000, place_type='real_estate_agency'):
    try:
        url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type={place_type}&key={GOOGLE_API_KEY}'
        response = requests.get(url)
        return response.json().get('results', [])
    except Exception as e:
        print(f"Error getting nearby places: {e}")
        return []


def get_place_details(place_id):
    try:
        url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={GOOGLE_API_KEY}'
        response = requests.get(url)
        return response.json().get('result', {})
    except Exception as e:
        print(f"Error getting place details: {e}")
        return {}


def web_scrape_information(place):
    query = place.replace(' ', '+') + '+real+estate+information'
    url = f'https://www.google.com/search?q={query}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Scraping logic here - this is a simplified example and might need adjustment
    information = {
        'safety': 'N/A',
        'population': 'N/A',
        'groceries_access': 'N/A',
        'entertainment': 'N/A',
        'avg_rent': 'N/A',
        'avg_buy_price': 'N/A'
    }

    # Scrape the information (the exact implementation will depend on the structure of the webpage)
    # For example:
    # safety_info = soup.find('div', {'class': 'safety-class'}).text
    # information['safety'] = safety_info if safety_info else 'N/A'

    # Returning mock data for demonstration
    information = {
        'safety': 'Safe neighborhood with low crime rates.',
        'population': 'Approximately 50,000 residents.',
        'groceries_access': 'Multiple grocery stores within a 1-mile radius.',
        'entertainment': 'Several cinemas, parks, and restaurants nearby.',
        'avg_rent': '$1,200 per month.',
        'avg_buy_price': '$300,000 on average.'
    }

    return information


def generate_map(PLACE, amenities_comparison):
    lat, lng = get_place_coordinates(PLACE)
    if lat is None or lng is None:
        return None

    map_ = folium.Map(location=[lat, lng], zoom_start=14)
    folium.Marker([lat, lng], tooltip='Target Location', popup=PLACE, icon=folium.Icon(color='red')).add_to(map_)

    for project in amenities_comparison:
        project_lat, project_lng = get_place_coordinates(project.get('formatted_address', ''))
        if project_lat is None or project_lng is None:
            continue
        folium.Marker(
            [project_lat, project_lng],
            tooltip=project.get('name', 'Unknown Name'),
            popup=f"{project.get('name', 'Unknown Name')}<br>{project.get('formatted_address', 'Unknown Address')}<br>{project.get('amenities', 'No amenities listed')}",
            icon=folium.Icon(color='blue')
        ).add_to(map_)

    data = BytesIO()
    map_.save(data, close_file=False)
    return data.getvalue().decode()


def display_selected_details(event):
    selected_indices = projects_listbox.curselection()
    selected_projects = [project_details[i] for i in selected_indices]

    if selected_projects:
        details_text.delete(1.0, tk.END)
        for project in selected_projects:
            details_text.insert(tk.END, f"Name: {project.get('name', 'N/A')}\n")
            details_text.insert(tk.END, f"Address: {project.get('formatted_address', 'N/A')}\n")
            details_text.insert(tk.END, f"Amenities: {project.get('amenities', 'No amenities listed')}\n\n")


def compare_selected_projects():
    selected_indices = projects_listbox.curselection()
    selected_projects = [project_details[i] for i in selected_indices]

    if selected_projects:
        comparison_text.delete(1.0, tk.END)
        comparison_text.insert(tk.END, compare_amenities_with_llm(selected_projects))


def format_information_with_llm(info):
    prompt = (
        "Format the following real estate information into a detailed, well-organized table:\n"
        f"Safety: {info['safety']}\n"
        f"Population: {info['population']}\n"
        f"Ease of Access to Groceries: {info['groceries_access']}\n"
        f"Entertainment: {info['entertainment']}\n"
        f"Average Rent: {info['avg_rent']}\n"
        f"Average Buying Price: {info['avg_buy_price']}\n"
    )

    # Using Hugging Face's summarization pipeline
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=512, min_length=50, length_penalty=2.0, num_beams=4,
                                 early_stopping=True)
    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return output.strip()


def compare_amenities_with_llm(projects):
    comparison_prompt = "Compare the following real estate projects in terms of area, safety, security, ease of access to groceries, and means of entertainment nearby:\n"
    for project in projects:
        comparison_prompt += f"Project Name: {project.get('name', 'N/A')}\n"
        comparison_prompt += f"Address: {project.get('formatted_address', 'N/A')}\n"
        comparison_prompt += f"Amenities: {project.get('amenities', 'No amenities listed')}\n\n"

    inputs = tokenizer(comparison_prompt, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=1024, min_length=100, length_penalty=2.0, num_beams=4,
                                 early_stopping=True)
    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return output.strip()


def analyze():
    PLACE = place_entry.get()
    if not PLACE:
        messagebox.showerror("Input Error", "Please enter a valid place.")
        return

    loading_label.grid(column=2, row=3, sticky=tk.W)
    root.update_idletasks()

    lat, lng = get_place_coordinates(PLACE)
    if lat is None or lng is None:
        loading_label.grid_remove()
        messagebox.showerror("Error", "Could not find the location. Please check the input.")
        return

    global project_details
    project_details = get_nearby_places(lat, lng)
    if not project_details:
        loading_label.grid_remove()
        messagebox.showerror("Error", "Could not find nearby projects.")
        return

    projects_listbox.delete(0, tk.END)
    for project in project_details:
        projects_listbox.insert(tk.END, project.get('name', 'Unknown Name'))

    place_information = web_scrape_information(PLACE)
    detailed_description = format_information_with_llm(place_information)

    comparison_text.delete(1.0, tk.END)
    comparison_text.insert(tk.END, detailed_description)

    map_html = generate_map(PLACE, project_details)
    if map_html is None:
        loading_label.grid_remove()
        messagebox.showerror("Error", "Could not generate the map.")
        return

    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as f:
        f.write(map_html.encode())
        webbrowser.open(f.name)

    loading_label.grid_remove()


root = tk.Tk()
root.title("Proplens - Real Estate Analysis")

mainframe = ttk.Frame(root, padding="10 10 20 20")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

place_label = ttk.Label(mainframe, text="Enter Place:")
place_label.grid(column=1, row=1, sticky=tk.W)
place_entry = ttk.Entry(mainframe, width=40)
place_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))

analyze_button = ttk.Button(mainframe, text="Analyze", command=analyze)
analyze_button.grid(column=2, row=2, sticky=tk.W)

projects_listbox = tk.Listbox(mainframe, selectmode=tk.MULTIPLE, height=10)
projects_listbox.grid(column=1, row=3, columnspan=2, sticky=(tk.W, tk.E))
projects_listbox.bind('<<ListboxSelect>>', display_selected_details)

details_text = scrolledtext.ScrolledText(mainframe, width=50, height=10)
details_text.grid(column=1, row=4, columnspan=2, sticky=(tk.W, tk.E))

compare_button = ttk.Button(mainframe, text="Compare Selected Projects", command=compare_selected_projects)
compare_button.grid(column=2, row=5, sticky=tk.W)

comparison_text = scrolledtext.ScrolledText(mainframe, width=50, height=10)
comparison_text.grid(column=1, row=6, columnspan=2, sticky=(tk.W, tk.E))

loading_label = ttk.Label(mainframe, text="Loading...")

root.mainloop()

