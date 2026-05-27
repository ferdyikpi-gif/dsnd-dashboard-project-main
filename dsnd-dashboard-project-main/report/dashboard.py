from fasthtml.common import *
import matplotlib.pyplot as plt

# Import QueryBase, Employee, Team from employee_events
from employee_events import Employee, Team

# import the load_model function from the utils.py file
from utils import load_model

"""
Below, we import the parent classes
you will use for subclassing
"""
from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
)

from combined_components import FormGroup, CombinedComponent


# Create a subclass of base_components/dropdown
# called `ReportDropdown`
class ReportDropdown(Dropdown):
    
    # Overwrite the build_component method
    # ensuring it has the same parameters
    # as the Report parent class's method
    def build_component(self, entity_id, model):
        #  Set the `label` attribute so it is set
        #  to the `name` attribute for the model
        self.label = f"Select {model.name.capitalize()}"
        
        # Return the output from the
        # parent class's build_component method
        return super().build_component(entity_id, model)
    
    # Overwrite the `component_data` method
    # Ensure the method uses the same parameters
    # as the parent class method
    def component_data(self, entity_id, model):
        # model.names() returns (full_name, id) for employees, (team_name, id) for teams
        raw = model.names()
        # Swap to (id, name) as expected by the Dropdown component
        return [(row[1], row[0]) for row in raw] if raw else []


# Create a subclass of base_components/BaseComponent
# called `Header`
class Header(BaseComponent):

    # Overwrite the `build_component` method
    # Ensure the method has the same parameters
    # as the parent class
    def build_component(self, entity_id, model):
        name_info = model.username(entity_id)
        if name_info and len(name_info) > 0:
            display_name = name_info[0][0]
        else:
            display_name = f"{model.name.capitalize()} #{entity_id}"
        return H1(f"Retention Dashboard - {display_name} ({model.name.capitalize()} Profile)")


# Create a subclass of base_components/MatplotlibViz
# called `LineChart`
class LineChart(MatplotlibViz):
    
    # Overwrite the parent class's `visualization`
    # method. Use the same parameters as the parent
    def visualization(self, entity_id, model):
        df = model.event_counts(entity_id)
        df = df.fillna(0).set_index('event_date').sort_index().cumsum()
        df.columns = ['Positive', 'Negative']
        
        fig, ax = plt.subplots(figsize=(6, 4))
        df.plot(ax=ax, marker='o')
        self.set_axis_styling(ax, bordercolor="black", fontcolor="black")
        ax.set_title("Cumulative Performance Events Over Time", fontsize=14)
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Event Log Counts")
        plt.tight_layout()
        return fig


# Create a subclass of base_components/MatplotlibViz
# called `BarChart`
class BarChart(MatplotlibViz):
    predictor = load_model()

    def visualization(self, entity_id, model):
        data = model.model_data(entity_id)
        if data.empty or data.fillna(0).values.sum() == 0:
            pred = 0.0
        else:
            probabilities = self.predictor.predict_proba(data)
            probs = probabilities[:, 1]
            pred = probs.mean() if model.name == "team" else probs[0]
        
        fig, ax = plt.subplots(figsize=(6, 1.5))
        ax.barh([''], [pred], color="crimson" if pred > 0.5 else "seagreen")
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        self.set_axis_styling(ax, bordercolor="black", fontcolor="black")
        return fig


# Create a subclass of combined_components/CombinedComponent
# called Visualizations       
class Visualizations(CombinedComponent):
    children = [LineChart(), BarChart()]
    outer_div_type = Div(cls='grid')


# Create a subclass of base_components/DataTable
# called `NotesTable`
class NotesTable(DataTable):
    def component_data(self, entity_id, model):
        return model.notes(entity_id)


class DashboardFilters(FormGroup):
    id = "top-filters"
    action = "/update_data"
    method="POST"
    children = [
        Radio(values=["Employee", "Team"], name='profile_type',
              hx_get='/update_dropdown', hx_target='#selector'),
        ReportDropdown(id="selector", name="user-selection")
    ]


# Create a subclass of CombinedComponents
# called `Report`
class Report(CombinedComponent):
    children = [Header(), DashboardFilters(), Visualizations(), NotesTable()]


# Initialize a fasthtml app 
app, rt = fast_app(hdrs=(Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"),))
report_view = Report()


@app.get("/")
def home():
    return report_view(1, Employee())


@app.get("/employee/{id}")
def employee_profile(id: str):
    return report_view(int(id), Employee())


@app.get("/team/{id}")
def team_profile(id: str):
    return report_view(int(id), Team())


@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    if r.query_params['profile_type'] == 'Team':
        return dropdown(None, Team())
    elif r.query_params['profile_type'] == 'Employee':
        return dropdown(None, Employee())


@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id_val = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id_val}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id_val}", status_code=303)


serve()
