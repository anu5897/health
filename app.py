#demo
from flask import Flask, request, render_template
import pickle
import numpy as np
import json
import pandas as pd


app = Flask(__name__)

#----------------- Load trained model-------------
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    le = pickle.load(f)  
#---------------LOAD CSV FILES----------------#
desc_df = pd.read_csv("data_desc.csv")
diet_df = pd.read_csv("diet.csv")

desc_df.columns = desc_df.columns.str.strip()
diet_df.columns = diet_df.columns.str.strip()

def clean_name(name):
    return str(name).lower().strip().replace(" ", "").replace("-", "")

# Clean disease names once
desc_df["clean"] = desc_df["Disease"].apply(clean_name)
diet_df["clean"] = diet_df["Disease"].apply(clean_name)

# SAME order as training(SYMPTOMS LIST)
symptoms_list = [
    "abnormal_menstruation","acidity","acute_liver_failure","aging_signs",
    "altered_sensorium","anemia","anxiety","back_pain","bladder_discomfort",
    "bleeding","bleeding_gums","blister","bloating","blood_in_sputum",
    "blood_in_urine","bloody_stool","blurred_vision","bone_pain",
    "breathing_problem","bruising","burping","chest_pain","chest_tightness",
    "chills","constipation","cough","cracked_lips","dark_urine",
    "dehydration","depression","diarrhea","difficulty_eating",
    "dischromic__patches","distention_of_abdomen","dizziness","dry_mouth",
    "drying_and_tingling_lips","dull_skin","easy_bruising",
    "enlarged_thyroid","eye_pain","fatigue","fever","fluid_overload",
    "foul_smell_of_urine","frequent_urination","gas","hair_loss",
    "headache","high_fever","increased_appetite","inflammatory_nails",
    "irregular_heartbeat","irritation","irritation_in_anus","itching",
    "joint_pain","loss_of_appetite","loss_of_smell","memory_loss",
    "mild_fever","milky_nipple_discharge","mood_swing","mouth_pain",
    "mouth_ulcers","movement_stiffness","muscle_loss","muscle_weakness",
    "nerve_pain","nerve_weakness","night_blindness","no_periods",
    "nodal_skin_eruptions","nosebleeds","numbness","obesity","pain",
    "pain_during_bowel_movements","pain_in_anal_region","pain_in_urination",
    "painful_walking","pale_skin","palpitations","patches_in_throat",
    "pelvic_pain","phlegm","poor_growth","prominent_veins_on_calf",
    "puffy_face_and_eyes","pus_filled_pimples","red_eyes","red_patch",
    "red_sore_around_nose","red_spot","restlessness","right_shoulder_pain",
    "runny_nose","scurring","sensitivity","shallow_breathing","shiverring",
    "silver_like_dusting","sinus_pressure","skin_peeling","skin_rash",
    "sleep_problems","slurred_speech","small_sores","sneezing","snoring",
    "sore_throat","spotting__urination","stiff_neck","stomach_bleeding",
    "stomach_pain","sunken_eyes","sweating","swelled_lymph_nodes",
    "swelling","swelling_in_neck","swelling_of_stomach","swollen_abdomen",
    "swollen_blood_vessels","swollen_extremeties","swollen_eyelids",
    "swollen_legs","throat_irritation","tooth_decay","toxic_look_(typhos)",
    "ulcers_on_tongue","vaginal_dryness","visual_disturbances","vomiting",
    "watery_eyes","weak_bones","weak_enamel","weak_immunity","weak_nails",
    "weakness","weight_gain","weight_loss","white_patch",
    "wound_slow_healing","yeast_infection","yellow_crust_ooze",
    "yellow_urine","yellowish_discharge","yellowish_eyes","yellowish_skin"
]
#------------------ROUTES-----------------------
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/pred")
def pred():
    symptoms = request.args.get("symptoms")

    if not symptoms:
        return render_template("pred.html",
                               disease="No symptoms selected",
                               selected=[],
                               description="",
                               diet=[],
                               avoid=[]
                               )

    selected_symptoms = json.loads(symptoms)

    # Create binary input vector
    input_vector = [1 if s in selected_symptoms else 0 for s in symptoms_list]
    input_array = np.array(input_vector).reshape(1, -1)

    # Predict
    pred_index = model.predict(input_array)[0]
    disease = le.inverse_transform([pred_index])[0]

    disease_clean = clean_name(disease)
     
    #if isinstance(pred_index, (int, np.integer)):
       # prediction = le.inverse_transform([pred_index])[0]
   # else:
    # Agar already string hai
        #prediction = pred_index

    # Description
    row = desc_df[desc_df["clean"] == disease_clean]
    description = row.iloc[0]["Description"] if not row.empty else "No description available."

     # Diet
    diet_row = diet_df[diet_df["clean"] == disease_clean]
    if not diet_row.empty:
        diet = diet_row.iloc[0]["Recommended Diet"].split(",")
        avoid = diet_row.iloc[0]["Avoid / Restrict"].split(",")
    else:
        diet, avoid = [], []


    return render_template(
        "pred.html",
        disease=disease,
        selected=selected_symptoms,
        description=description,
        diet=diet,
        avoid=avoid
    )


if __name__ == "__main__":
    app.run(debug=True)
