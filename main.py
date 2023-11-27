import streamlit as st
from linkedin_api import Linkedin
import json

def authenticate_linkedin(username, password):
    try:
        api = Linkedin(username=username, password=password)
        return api
    except json.JSONDecodeError:
        st.error("Authentication failed. Please check your LinkedIn credentials.")
        return None

def search_linkedin(api, first_name, last_name, company_names, years_of_service):
    search_results = api.search_people(f"{first_name} {last_name}")
    
    for result in search_results:
        profile_id = result['publicIdentifier']
        profile = api.get_profile(profile_id=profile_id)
        
        if match_criteria(profile, company_names, years_of_service):
            st.success(f"Match found! LinkedIn URL: [https://www.linkedin.com/in/{profile_id}](https://www.linkedin.com/in/{profile_id})")
            return
    
    st.warning("No matching profile found on LinkedIn.")

def match_criteria(profile, company_names, years_of_service):
    experience = profile['experience']
    
    for job in experience:
        company_name = job['companyName']
        start_date = job.get('timePeriod', {}).get('startDate', {}).get('year')
        end_date = job.get('timePeriod', {}).get('endDate', {}).get('year')
        
        if company_name in company_names and is_years_of_service_match(start_date, end_date, years_of_service):
            return True
    
    return False

def is_years_of_service_match(start_date, end_date, years_of_service):
    return True

def main():
    st.title("LinkedIn Profile Search")
    st.sidebar.header("Input Variables")

    first_name = st.sidebar.text_input("First Name")
    last_name = st.sidebar.text_input("Last Name")
    company_names = st.sidebar.text_input("Company Name(s) (comma-separated)").split(',')
    years_of_service = st.sidebar.number_input("Years of Service", min_value=0, max_value=50)

    username = st.sidebar.text_input("LinkedIn Username")
    password = st.sidebar.text_input("LinkedIn Password", type="password")

    if st.sidebar.button("Authenticate and Search LinkedIn"):
        with st.spinner("Authenticating with LinkedIn..."):
            api = authenticate_linkedin(username, password)
            if api:
                with st.spinner("Searching LinkedIn..."):
                    search_linkedin(api, first_name, last_name, company_names, years_of_service)

if __name__ == "__main__":
    main()
