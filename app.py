import streamlit as st

# --- Configuration based on your requirements ---
SUBJECTS_CONFIG = [
    {"name": "BDD",     "cc_pct": 0.4, "exam_pct": 0.6, "coef": 5},
    {"name": "ML",      "cc_pct": 0.5, "exam_pct": 0.5, "coef": 4},
    {"name": "IC",      "cc_pct": 0.4, "exam_pct": 0.6, "coef": 4},
    {"name": "SEDS",    "cc_pct": 0.5, "exam_pct": 0.5, "coef": 4},
    {"name": "MATHav",  "cc_pct": 0.6, "exam_pct": 0.4, "coef": 3},
    {"name": "COMP",    "cc_pct": 0.4, "exam_pct": 0.6, "coef": 3},
    {"name": "Network", "cc_pct": 0.4, "exam_pct": 0.6, "coef": 2},
    {"name": "IHM",     "cc_pct": 0.5, "exam_pct": 0.5, "coef": 2},
    {"name": "Stage",   "cc_pct": 0.0, "exam_pct": 1.0, "coef": 2},
]

# --- App Interface ---
st.set_page_config(page_title="Semester 1 Calculator", page_icon="🎓")

st.title("🎓 Semester 1 Average Calculator")
st.write("Enter your grades (**0** to **20**) for each module below. The app handles the coefficients and CC/Exam percentages automatically.")

st.divider()

# Column Headers
col1, col2, col3 = st.columns([2, 1, 1])
col1.markdown("**Module & Coefficient**")
col2.markdown("**CC Grade**")
col3.markdown("**Exam Grade**")

st.divider()

grades = {}

# Generate input rows dynamically
for sub in SUBJECTS_CONFIG:
    c1, c2, c3 = st.columns([2, 1, 1])
    name = sub["name"]
    coef = sub["coef"]
    
    # Display Module Name
    c1.write(f"**{name}** (Coef {coef})")
    
    # Handle Inputs
    if name == "Stage":
        # Disable CC for Stage
        cc_val = c2.number_input(f"CC {name}", min_value=0.0, max_value=20.0, value=0.0, step=0.25, disabled=True, label_visibility="collapsed")
        exam_val = c3.number_input(f"Exam {name}", min_value=0.0, max_value=20.0, value=0.0, step=0.25, label_visibility="collapsed")
    else:
        cc_val = c2.number_input(f"CC {name}", min_value=0.0, max_value=20.0, value=0.0, step=0.25, label_visibility="collapsed")
        exam_val = c3.number_input(f"Exam {name}", min_value=0.0, max_value=20.0, value=0.0, step=0.25, label_visibility="collapsed")
        
    # Store the inputted values
    grades[name] = {"cc": cc_val, "exam": exam_val, "config": sub}

st.divider()

# --- Calculation Logic ---
if st.button("Calculate My Average", type="primary", use_container_width=True):
    total_weighted_score = 0
    total_coefficients = 0
    
    for name, data in grades.items():
        config = data['config']
        cc_score = data['cc']
        exam_score = data['exam']
        
        # Apply specific module logic
        if name == "Stage":
            module_avg = exam_score # 100% Exam
        else:
            module_avg = (cc_score * config['cc_pct']) + (exam_score * config['exam_pct'])
            
        # Accumulate totals
        total_weighted_score += module_avg * config['coef']
        total_coefficients += config['coef']
        
    # Final Math
    if total_coefficients > 0:
        semester_avg = total_weighted_score / total_coefficients
        
        # Display Results
        st.subheader("Your Results")
        
        if semester_avg >= 10:
            st.success(f"### 🎉 Final Average: {semester_avg:.2f} / 20")
            st.balloons() # Fun little animation for passing!
        else:
            st.error(f"### ⚠️ Final Average: {semester_avg:.2f} / 20")
            
        st.info(f"**Total Points:** {total_weighted_score:.2f} out of {total_coefficients * 20}")