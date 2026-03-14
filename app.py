import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import time

# Page Configuration
st.set_page_config(
    page_title="AquaSphere - Smart Aquarium Monitor",
    page_icon="🐠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .warning-box {
        background-color: #ff4b4b;
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .success-box {
        background-color: #00cc66;
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'aquarium_data' not in st.session_state:
    st.session_state.aquarium_data = {
        'temperature': [],
        'pH': [],
        'turbidity': [],
        'water_level': [],
        'timestamps': []
    }
if 'feeding_schedule' not in st.session_state:
    st.session_state.feeding_schedule = []
if 'alerts' not in st.session_state:
    st.session_state.alerts = []

# Sidebar Navigation
st.sidebar.image("https://via.placeholder.com/150x150.png?text=AquaSphere", use_container_width=True)
st.sidebar.title("🐠 AquaSphere")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Water Quality", "Feeding System", "Lighting Control", 
     "Health Monitoring", "Reports", "Settings"]
)

# Generate simulated sensor data
def generate_sensor_data():
    return {
        'temperature': round(random.uniform(24.0, 28.0), 1),
        'pH': round(random.uniform(6.8, 7.4), 2),
        'turbidity': round(random.uniform(0.5, 5.0), 1),
        'water_level': round(random.uniform(85.0, 100.0), 1),
        'dissolved_oxygen': round(random.uniform(6.0, 9.0), 1),
        'ammonia': round(random.uniform(0.0, 0.25), 3),
        'nitrite': round(random.uniform(0.0, 0.1), 3),
        'nitrate': round(random.uniform(0.0, 20.0), 1)
    }

# Update data in session state
def update_data():
    new_data = generate_sensor_data()
    timestamp = datetime.now()
    
    # Keep last 24 hours of data (assuming updates every minute)
    if len(st.session_state.aquarium_data['timestamps']) >= 1440:
        for key in st.session_state.aquarium_data:
            st.session_state.aquarium_data[key].pop(0)
    
    for key in new_data:
        if key in st.session_state.aquarium_data:
            st.session_state.aquarium_data[key].append(new_data[key])
        else:
            st.session_state.aquarium_data[key] = [new_data[key]]
    
    st.session_state.aquarium_data['timestamps'].append(timestamp)
    
    # Check for alerts
    check_alerts(new_data)
    
    return new_data

# Check for alerts
def check_alerts(data):
    alerts = []
    
    if data['temperature'] > 28:
        alerts.append(f"⚠️ High Temperature: {data['temperature']}°C")
    elif data['temperature'] < 24:
        alerts.append(f"⚠️ Low Temperature: {data['temperature']}°C")
    
    if data['pH'] > 7.4:
        alerts.append(f"⚠️ High pH: {data['pH']}")
    elif data['pH'] < 6.8:
        alerts.append(f"⚠️ Low pH: {data['pH']}")
    
    if data['turbidity'] > 4:
        alerts.append(f"⚠️ High Turbidity: {data['turbidity']} NTU")
    
    if data['water_level'] < 90:
        alerts.append(f"⚠️ Low Water Level: {data['water_level']}%")
    
    if data['ammonia'] > 0.2:
        alerts.append(f"⚠️ High Ammonia: {data['ammonia']} ppm")
    
    if alerts:
        st.session_state.alerts = alerts
    else:
        st.session_state.alerts = ["✅ All parameters normal"]

# Dashboard
if menu == "Dashboard":
    st.markdown('<div class="main-header"><h1>🏠 AquaSphere Dashboard</h1></div>', unsafe_allow_html=True)
    
    # Auto-refresh
    refresh = st.checkbox("Auto-refresh (5 seconds)")
    if refresh:
        time.sleep(5)
        st.rerun()
    
    # Get current data
    current_data = generate_sensor_data()
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🌡️ Temperature", f"{current_data['temperature']}°C", 
                 f"{random.uniform(-0.5, 0.5):.1f}°C")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🧪 pH Level", current_data['pH'],
                 f"{random.uniform(-0.1, 0.1):.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("💧 Dissolved O₂", f"{current_data['dissolved_oxygen']} mg/L",
                 f"{random.uniform(-0.2, 0.2):.1f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("📊 Water Level", f"{current_data['water_level']}%",
                 f"{random.uniform(-1, 1):.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Alerts
    st.markdown("### 🚨 Current Alerts")
    check_alerts(current_data)
    for alert in st.session_state.alerts:
        if "✅" in alert:
            st.markdown(f'<div class="success-box">{alert}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="warning-box">{alert}</div>', unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Temperature Trend")
        # Simulate historical data
        hours = list(range(24))
        temps = [random.uniform(24, 28) for _ in range(24)]
        fig = px.line(x=hours, y=temps, labels={'x': 'Hours Ago', 'y': 'Temperature (°C)'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 pH Level Trend")
        ph_values = [random.uniform(6.8, 7.4) for _ in range(24)]
        fig = px.line(x=hours, y=ph_values, labels={'x': 'Hours Ago', 'y': 'pH Level'})
        st.plotly_chart(fig, use_container_width=True)

# Water Quality
elif menu == "Water Quality":
    st.markdown('<div class="main-header"><h1>💧 Water Quality Monitoring</h1></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Current Parameters")
        data = generate_sensor_data()
        
        quality_data = pd.DataFrame({
            'Parameter': ['Temperature', 'pH', 'Turbidity', 'Dissolved Oxygen', 
                         'Ammonia', 'Nitrite', 'Nitrate', 'Water Level'],
            'Value': [f"{data['temperature']} °C", data['pH'], 
                     f"{data['turbidity']} NTU", f"{data['dissolved_oxygen']} mg/L",
                     f"{data['ammonia']} ppm", f"{data['nitrite']} ppm",
                     f"{data['nitrate']} ppm", f"{data['water_level']}%"],
            'Status': ['Good' if 24 <= data['temperature'] <= 28 else 'Warning',
                      'Good' if 6.8 <= data['pH'] <= 7.4 else 'Warning',
                      'Good' if data['turbidity'] <= 4 else 'Warning',
                      'Good' if data['dissolved_oxygen'] >= 6 else 'Warning',
                      'Good' if data['ammonia'] <= 0.2 else 'Warning',
                      'Good' if data['nitrite'] <= 0.1 else 'Warning',
                      'Good' if data['nitrate'] <= 20 else 'Warning',
                      'Good' if data['water_level'] >= 90 else 'Warning']
        })
        
        st.dataframe(quality_data, use_container_width=True)
    
    with col2:
        st.markdown("### Water Quality Index")
        
        # Calculate WQI (simplified)
        wqi = 100 - (abs(data['temperature'] - 26) * 2 + 
                    abs(data['pH'] - 7.1) * 20 +
                    data['turbidity'] * 2 +
                    data['ammonia'] * 200)
        wqi = max(0, min(100, wqi))
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = wqi,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Water Quality Score"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "red"},
                    {'range': [50, 75], 'color': "yellow"},
                    {'range': [75, 100], 'color': "green"}
                ]
            }))
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Historical data
    st.markdown("### 📊 Historical Analysis")
    days = st.selectbox("Select time range", ["Last 24 Hours", "Last 7 Days", "Last 30 Days"])
    
    # Simulate historical data
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    hist_data = pd.DataFrame({
        'Date': dates,
        'Temperature': [random.uniform(24, 28) for _ in range(30)],
        'pH': [random.uniform(6.8, 7.4) for _ in range(30)],
        'Turbidity': [random.uniform(0.5, 5) for _ in range(30)]
    })
    
    fig = px.line(hist_data, x='Date', y=['Temperature', 'pH', 'Turbidity'],
                  title="Water Quality Trends")
    st.plotly_chart(fig, use_container_width=True)

# Feeding System
elif menu == "Feeding System":
    st.markdown('<div class="main-header"><h1>🍕 Automated Feeding System</h1></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Manual Feeding")
        
        if st.button("🎯 Feed Now", use_container_width=True):
            st.success("✅ Feeding initiated! Food dispensed.")
        
        st.markdown("### Feeding Schedule")
        
        # Add new schedule
        with st.expander("➕ Add New Schedule"):
            feed_time = st.time_input("Feeding Time", datetime.now().time())
            feed_amount = st.slider("Food Amount (grams)", 1, 20, 5)
            feed_type = st.selectbox("Food Type", ["Flakes", "Pellets", "Freeze-dried"])
            
            if st.button("Add to Schedule"):
                new_schedule = {
                    'time': feed_time.strftime("%H:%M"),
                    'amount': feed_amount,
                    'type': feed_type,
                    'enabled': True
                }
                st.session_state.feeding_schedule.append(new_schedule)
                st.success("✅ Schedule added!")
    
    with col2:
        st.markdown("### Current Schedule")
        
        # Display existing schedules
        if st.session_state.feeding_schedule:
            for i, schedule in enumerate(st.session_state.feeding_schedule):
                col_a, col_b, col_c = st.columns([2, 2, 1])
                with col_a:
                    st.write(f"🕐 {schedule['time']}")
                with col_b:
                    st.write(f"📦 {schedule['amount']}g - {schedule['type']}")
                with col_c:
                    if st.button(f"❌", key=f"del_{i}"):
                        st.session_state.feeding_schedule.pop(i)
                        st.rerun()
        else:
            st.info("No feeding schedules set. Add one using the form.")
        
        st.markdown("### 📊 Feeding Statistics")
        
        # Statistics
        total_food = sum([s['amount'] for s in st.session_state.feeding_schedule]) if st.session_state.feeding_schedule else 0
        
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        metrics_col1.metric("Daily Feedings", len(st.session_state.feeding_schedule))
        metrics_col2.metric("Total Food/Day", f"{total_food}g")
        metrics_col3.metric("Next Feeding", 
                           st.session_state.feeding_schedule[0]['time'] if st.session_state.feeding_schedule else "Not set")

# Lighting Control
elif menu == "Lighting Control":
    st.markdown('<div class="main-header"><h1>💡 Smart Lighting Control</h1></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Manual Control")
        
        # Light status
        light_on = st.toggle("Lights", value=True)
        
        if light_on:
            brightness = st.slider("Brightness", 0, 100, 80)
            color_temp = st.select_slider("Color Temperature", 
                                         options=["Warm", "Neutral", "Cool"],
                                         value="Neutral")
            
            st.markdown(f"**Current Settings:**")
            st.markdown(f"- Status: {'ON' if light_on else 'OFF'}")
            st.markdown(f"- Brightness: {brightness}%")
            st.markdown(f"- Color: {color_temp}")
    
    with col2:
        st.markdown("### Automatic Schedule")
        
        # Sunrise/Sunset simulation
        st.markdown("#### Sunrise/Sunset Times")
        sunrise = st.time_input("Sunrise", datetime.strptime("06:00", "%H:%M").time())
        sunset = st.time_input("Sunset", datetime.strptime("18:00", "%H:%M").time())
        
        st.markdown("#### Lighting Profile")
        profile = st.selectbox("Lighting Mode", 
                              ["Natural Daylight", "Moonlight", "Plant Growth", "Custom"])
        
        if profile == "Natural Daylight":
            st.info("🌅 Gradual brightening at sunrise, dimming at sunset")
        elif profile == "Moonlight":
            st.info("🌙 Low blue light for nighttime viewing")
        elif profile == "Plant Growth":
            st.info("🌱 Full spectrum for aquatic plants")
    
    # Lighting schedule visualization
    st.markdown("### 📅 Daily Light Cycle")
    
    # Simulate light intensity throughout the day
    hours = list(range(24))
    intensity = [0 if h < 6 or h > 18 else min(100, (h-6)*16.7) for h in hours]
    
    fig = px.area(x=hours, y=intensity, 
                 labels={'x': 'Hour of Day', 'y': 'Light Intensity %'},
                 title="Light Schedule")
    st.plotly_chart(fig, use_container_width=True)

# Health Monitoring
elif menu == "Health Monitoring":
    st.markdown('<div class="main-header"><h1>🐟 Fish Health Monitoring</h1></div>', unsafe_allow_html=True)
    
    # Fish population
    st.markdown("### Current Population")
    
    col1, col2, col3, col4 = st.columns(4)
    
    fish_data = {
        "Neon Tetras": {"count": 12, "health": "Good"},
        "Guppies": {"count": 8, "health": "Good"},
        "Corydoras": {"count": 6, "health": "Warning"},
        "Angelfish": {"count": 4, "health": "Good"}
    }
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🐠 Neon Tetras", fish_data["Neon Tetras"]["count"])
        st.markdown(f"Health: ✅ Good")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🐡 Guppies", fish_data["Guppies"]["count"])
        st.markdown(f"Health: ✅ Good")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🐟 Corydoras", fish_data["Corydoras"]["count"])
        st.markdown(f'Health: ⚠️ Warning')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🐠 Angelfish", fish_data["Angelfish"]["count"])
        st.markdown(f"Health: ✅ Good")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Health alerts
    st.markdown("### 🚨 Health Alerts")
    
    alerts_data = [
        {"species": "Corydoras", "issue": "Reduced activity", "severity": "Medium", "time": "2 hours ago"},
        {"species": "All", "issue": "Water change needed", "severity": "Low", "time": "1 day ago"}
    ]
    
    for alert in alerts_data:
        if alert["severity"] == "Medium":
            st.markdown(f'<div class="warning-box">⚠️ {alert["species"]}: {alert["issue"]} ({alert["time"]})</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="success-box">ℹ️ {alert["species"]}: {alert["issue"]} ({alert["time"]})</div>', 
                       unsafe_allow_html=True)
    
    # Behavior analysis
    st.markdown("### 📊 Behavior Analysis")
    
    behavior_data = pd.DataFrame({
        'Time': ['Morning', 'Afternoon', 'Evening', 'Night'],
        'Activity Level': [85, 70, 90, 30],
        'Feeding Response': [90, 60, 95, 20]
    })
    
    fig = px.line(behavior_data, x='Time', y=['Activity Level', 'Feeding Response'],
                  title="Fish Activity Patterns")
    st.plotly_chart(fig, use_container_width=True)

# Reports
elif menu == "Reports":
    st.markdown('<div class="main-header"><h1>📊 Reports & Analytics</h1></div>', unsafe_allow_html=True)
    
    # Report generation options
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Generate Report")
        
        report_type = st.selectbox("Report Type", 
                                  ["Daily Summary", "Weekly Analysis", "Monthly Report", "Custom Range"])
        
        if report_type == "Custom Range":
            start_date = st.date_input("Start Date", datetime.now() - timedelta(days=7))
            end_date = st.date_input("End Date", datetime.now())
        else:
            st.info(f"Generating {report_type}")
        
        include_sections = st.multiselect(
            "Include Sections",
            ["Water Quality", "Feeding Log", "Lighting Schedule", "Health Metrics", "Alerts"],
            default=["Water Quality", "Feeding Log", "Alerts"]
        )
        
        if st.button("📄 Generate Report", use_container_width=True):
            st.success("Report generated successfully! Download available below.")
    
    with col2:
        st.markdown("### Quick Statistics")
        
        # Generate some statistics
        stats_data = {
            "Average Temperature": "26.2°C",
            "Average pH": "7.1",
            "Total Feedings": "42",
            "Alerts Triggered": "3",
            "Water Changes": "2",
            "System Uptime": "99.8%"
        }
        
        for key, value in stats_data.items():
            st.markdown(f"**{key}:** {value}")
    
    # Sample report preview
    st.markdown("### 📋 Report Preview")
    
    # Create sample report data
    report_dates = pd.date_range(end=datetime.now(), periods=7, freq='D')
    report_data = pd.DataFrame({
        'Date': report_dates,
        'Avg Temperature': [random.uniform(25, 27) for _ in range(7)],
        'Avg pH': [random.uniform(6.9, 7.3) for _ in range(7)],
        'Feedings': [random.randint(2, 4) for _ in range(7)],
        'Alerts': [random.randint(0, 2) for _ in range(7)]
    })
    
    st.dataframe(report_data, use_container_width=True)
    
    # Export options
    st.markdown("### 📥 Export Options")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 CSV", use_container_width=True):
            st.success("CSV file downloaded!")
    
    with col2:
        if st.button("📑 PDF", use_container_width=True):
            st.success("PDF report downloaded!")
    
    with col3:
        if st.button("📧 Email Report", use_container_width=True):
            st.success("Report emailed successfully!")

# Settings
elif menu == "Settings":
    st.markdown('<div class="main-header"><h1>⚙️ System Settings</h1></div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["General", "Notifications", "Device Management", "User Profile"])
    
    with tabs[0]:
        st.markdown("### General Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Aquarium Info")
            tank_name = st.text_input("Tank Name", "My Aquarium")
            tank_size = st.number_input("Tank Size (gallons)", 10, 200, 50)
            tank_type = st.selectbox("Tank Type", ["Freshwater", "Saltwater", "Brackish"])
            
            st.markdown("#### Measurement Units")
            units = st.radio("Units", ["Metric (°C, L)", "Imperial (°F, gal)"])
        
        with col2:
            st.markdown("#### Alert Thresholds")
            temp_min = st.slider("Min Temperature (°C)", 20, 30, 24)
            temp_max = st.slider("Max Temperature (°C)", 20, 30, 28)
            ph_min = st.slider("Min pH", 6.0, 8.0, 6.8)
            ph_max = st.slider("Max pH", 6.0, 8.0, 7.4)
    
    with tabs[1]:
        st.markdown("### Notification Settings")
        
        st.markdown("#### Enable Notifications For:")
        email_notify = st.checkbox("Email Notifications", True)
        push_notify = st.checkbox("Push Notifications", True)
        sms_notify = st.checkbox("SMS Notifications", False)
        
        st.markdown("#### Alert Types")
        col1, col2 = st.columns(2)
        
        with col1:
            temp_alerts = st.checkbox("Temperature Alerts", True)
            ph_alerts = st.checkbox("pH Alerts", True)
            water_level_alerts = st.checkbox("Water Level Alerts", True)
        
        with col2:
            feeding_alerts = st.checkbox("Feeding Reminders", True)
            maintenance_alerts = st.checkbox("Maintenance Reminders", True)
            health_alerts = st.checkbox("Health Alerts", True)
        
        if email_notify:
            st.markdown("#### Email Settings")
            email = st.text_input("Email Address", "user@example.com")
    
    with tabs[2]:
        st.markdown("### Connected Devices")
        
        devices = {
            "Temperature Sensor": "Online",
            "pH Sensor": "Online",
            "Water Level Sensor": "Online",
            "Feeder": "Online",
            "Light Controller": "Online",
            "Camera": "Offline"
        }
        
        for device, status in devices.items():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(device)
            with col2:
                color = "green" if status == "Online" else "red"
                st.markdown(f":{color}[{status}]")
            with col3:
                if st.button(f"Configure", key=f"cfg_{device}"):
                    st.info(f"Configuring {device}...")
    
    with tabs[3]:
        st.markdown("### User Profile")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Personal Information")
            name = st.text_input("Full Name", "John Doe")
            username = st.text_input("Username", "johndoe")
            email_profile = st.text_input("Email", "john@example.com")
        
        with col2:
            st.markdown("#### Change Password")
            old_pass = st.text_input("Current Password", type="password")
            new_pass = st.text_input("New Password", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")
        
        if st.button("Save Changes", use_container_width=True):
            st.success("Settings saved successfully!")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### System Status")
st.sidebar.info("🟢 All Systems Online")
st.sidebar.markdown(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")