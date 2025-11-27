import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import List, Dict, Tuple

class SocialMediaSimulator:
    """
    Advanced social media data simulator with multilingual support (English/Sheng/Swahili),
    sentiment analysis, and comprehensive community issues coverage.
    """
    
    def __init__(self, seed: int = 42):
        """Initialize simulator with enhanced parameters"""
        random.seed(seed)
        np.random.seed(seed)
        
        # Expanded usernames (50+ variations)
        self.usernames = [
            "ConcernedCitizen", "LocalResident123", "CommunityWatch", "NairobiNative",
            "UrbanObserver", "CityDweller", "SafetyFirst", "HealthAdvocate",
            "InfraAlert", "PublicVoice", "GovAccountability", "NeighborhoodEyes",
            "ServiceMonitor", "QualityOfLife", "ResidentUnion", "CivicWatch",
            "StreetLevel", "PeopleFirst", "LocalActivist", "CommunityMatters",
            "CitizenReporter", "UrbanIssues", "MyNeighborhood", "AreaResident",
            "TownHall", "WanjikuSpeaks", "MtuWaGround", "NairobiVibes",
            "KiberaWatch", "EastleighNews", "WestlandsResident", "KarenLife",
            "MathareCitizen", "EmbkasiVoice", "KasaraniResident", "DagorettiWatch",
            "RuarakaResident", "UmojaUnited", "HurumaHealth", "RoysambuRising",
            "ThikaRoadAlert", "KangundoWatch", "LangataLife", "ForestRoadResident",
            "WaiyakiWatch", "JogooRoadAlert", "MountainViewResident", "PipelineVoice",
            "BuruburuResident", "DonaholmWatch", "KayoleAlert", "ZimmermanVoice"
        ]
        
        # Comprehensive issue categories (20+ categories)
        self.issue_templates = {
            "water_supply": [
                "Maji imekatwa {location} for {days} days. Tunaomba serikali msaada! {urgency}",
                "Water shortage in {location} for {days} days now. Families struggling. {urgency}",
                "Hakuna maji {location} tangu juzi. Tunalipaje karo ya maji bila service?",
                "No water in {location} for a week. Kids can't go to school clean. {urgency}",
                "Water tanker prices in {location} imepanda x3. Exploitation during crisis!",
                "Maji ya brown color inatoka kwa pipe {location}. Is this safe to drink? {urgency}",
                "{location} residents fetching water from river. Health hazard! {urgency}",
                "Borehole in {location} dried up. Community needs water solutions ASAP!",
                "Water rationing in {location} insufficient. We get maji once per week only.",
                "Hakuna water supply {location} for {days} days. Watu wanateseka sana."
            ],
            
            "electricity": [
                "Umeme imeenda {location} for {time}. Biashara zimefunga. Tutado? {urgency}",
                "Power outage {location} since {time}. Food spoiling, businesses closed. {urgency}",
                "Daily blackouts in {location}. 3-4 times a day! How do we survive like this?",
                "Kenya Power ignoring {location}. Transformer burst last week, still no fix!",
                "Stima za prepaid {location} zinaisha haraka sana. Corruption? Meter fraud?",
                "No electricity {location} for {days} days. Students can't study at night.",
                "Power surge in {location} destroyed appliances. Who compensates us? {urgency}",
                "Illegal connections in {location} causing blackouts. KPLC must act! {urgency}",
                "Transformer vandalized in {location}. Area in darkness for days.",
                "Frequent power cuts {location} affecting hospital operations. Lives at risk! {urgency}"
            ],
            
            "roads_infrastructure": [
                "Road to {location} ni shida mob. Magari zinaharibika daily. {urgency}",
                "Massive pothole on {street} causing accidents. 2 cars damaged today! {urgency}",
                "Bridge on {street} has cracks. Very dangerous. Inspectors needed ASAP!",
                "{location} road flooded. Impassable during rain. When will county fix this?",
                "Dust from {street} road unbearable. Respiratory issues on the rise.",
                "No road markings on {street}. Accidents waiting to happen! {urgency}",
                "Construction on {street} abandoned for 2 years. Wasted taxpayer money!",
                "Speed bumps on {street} destroying vehicles. Who approved this design?",
                "Drainage blocked on {street}. Road floods every rain. Poor planning!",
                "{location} road completely damaged. Bodabodas can't even pass through."
            ],
            
            "sewage_drainage": [
                "Sewage overflow {location}. Maji chafu everywhere. Kids playing in it! {urgency}",
                "Blocked drainage in {location} causing floods. Houses submerged during rain.",
                "Raw sewage flowing on {street}. Health hazard! County must act now! {urgency}",
                "Manhole cover missing on {street}. Child almost fell in yesterday! {urgency}",
                "Drainage system {location} hasn't been cleaned in years. Smells terrible.",
                "Sewage burst in {location} flooding homes. Emergency situation! {urgency}",
                "Open sewer {location} attracting rats and disease. This is unacceptable!",
                "Storm water mixed with sewage {location}. Contamination risk! {urgency}",
                "No proper drainage in {location}. Roads become rivers during rain.",
                "Sewage tanker dumping waste illegally near {location}. Report to NEMA!"
            ],
            
            "healthcare_facilities": [
                "Hospital {location} hakuna dawa. Patients wanarudi nyumbani bila treatment. {urgency}",
                "Clinic shortage in {location}. Nearest hospital is 20km away!",
                "No doctors at {location} health center for 3 days. What's happening?",
                "Medical emergency {location} but ambulance took 2+ hours! {urgency}",
                "Pregnant mama denied care at {location} hospital. Bed shortage. Critical! {urgency}",
                "Medicine stockout at {location}. Diabetic and HIV patients suffering. {urgency}",
                "Long queues at {location} hospital. 8+ hours wait for basic care!",
                "No pediatrician in {location}. Children's health at risk.",
                "Equipment broken at {location} hospital. X-ray machine down for months.",
                "Healthcare workers on strike {location}. Patients being turned away. {urgency}"
            ],
            
            "education": [
                "School in {location} has no teachers for math and science. Kids suffering.",
                "Overcrowded classes in {location}. 100+ students per class! Quality?",
                "School building {location} ni dangerous. Cracks on walls. Collapse risk! {urgency}",
                "No desks in {location} school. Kids sit on floor. This is 2025!",
                "Teachers strike in {location}. Kids home for 2 weeks. When will this end?",
                "School fees increased 50% in {location}. Parents can't afford. Education rights?",
                "No toilets working in {location} school. Hygiene crisis! {urgency}",
                "School feeding program stopped {location}. Kids coming to school hungry.",
                "Textbooks shortage in {location}. 5 kids sharing 1 book. How will they learn?",
                "Security issues at {location} school. Drug dealers near gate. Parents worried! {urgency}"
            ],
            
            "security_crime": [
                "Increased crime {location}. 3 robberies this week. Police patrol needed! {urgency}",
                "Gang activity reported {location}. Residents living in fear every night.",
                "No police patrols {location} at night. Community feeling very unsafe.",
                "Mugging incidents {location} increasing. Women afraid to walk after 7pm.",
                "Hit and run on {street}. Driver escaped. Anyone with info? {urgency}",
                "Carjacking attempt {location} today. 3rd incident this month! {urgency}",
                "Vigilante mob justice {location} yesterday. Rule of law breaking down.",
                "Drug dealing in broad daylight {location}. Police do nothing!",
                "House break-ins {location} every week. Thieves operating freely.",
                "Sexual harassment cases rising {location}. Women need protection! {urgency}"
            ],
            
            "fire_emergency": [
                "Fire outbreak {location} market! Emergency response needed NOW! {urgency}",
                "Slum fire {location} destroying homes. Families homeless. Help! {urgency}",
                "Gas explosion {location} today. Multiple injuries. Ambulances needed! {urgency}",
                "No fire extinguishers in {location} buildings. Fire safety ignored!",
                "Fire station {location} has no water. How will they fight fires? {urgency}",
                "Electrical fire {location} due to illegal connections. Lives lost.",
                "Fire destroyed {location} school. Kids have nowhere to learn now.",
                "Factory fire {location} still burning. No fire engines! Where's response? {urgency}",
                "Cooking gas explosions increasing {location}. Counterfeit cylinders? {urgency}",
                "Bush fire near {location} residential area. Homes at risk! {urgency}"
            ],
            
            "garbage_sanitation": [
                "Garbage piles {location} for weeks. Takataka everywhere. County sleeping?",
                "Overflowing dumpsite {location}. Burning plastic daily. Air pollution! {urgency}",
                "No garbage collection {location} for 1 month. Health hazard sasa! {urgency}",
                "Street cleaners on strike {location}. Streets full of trash.",
                "Illegal dumping {location} at night. Trucks bringing waste from other areas!",
                "Garbage blocking drainage {location}. Floods incoming with rain. {urgency}",
                "Recycling program {location} collapsed. Waste management disaster.",
                "Dumped medical waste {location}. Needles and syringes on street! {urgency}",
                "Plastics clogging river near {location}. Environmental catastrophe!",
                "No dustbins on {street}. People forced to litter. Provide bins!"
            ],
            
            "public_transport": [
                "Matatu cartel {location} increasing fares daily. Exploitation! {urgency}",
                "Bus terminus {location} ni shida. No toilets, no shelter, no safety.",
                "Reckless driving on {street}. Matatus causing accidents daily! {urgency}",
                "No pedestrian crossing on {street}. People dying trying to cross! {urgency}",
                "Matatu strike {location}. Workers stranded. When will this end?",
                "Boda boda riders {location} overcharging visitors. Cartels in operation!",
                "Bus station {location} full of thugs. Passengers getting mugged. {urgency}",
                "Overcrowded matatus {location}. Carrying 20+ people in 14-seater!",
                "No bus service to {location} at night. How do night shift workers commute?",
                "Traffic jam {street} daily. 3 hours to travel 5km. Infrastructure failure!"
            ],
            
            "housing": [
                "Illegal demolitions {location} today. Families homeless in rain! {urgency}",
                "Rent increased 30% in {location}. Where will low-income families go?",
                "Landlord harassment {location}. Threats and intimidation daily.",
                "No affordable housing {location}. Working families priced out!",
                "Building collapse {location}! Trapped people inside. Rescue needed! {urgency}",
                "Slum upgrading {location} stalled. Project abandoned halfway.",
                "Unsafe buildings {location}. County allowing construction without permits!",
                "Eviction notice {location}. 500 families being displaced. Where will they go?",
                "Housing scam {location}. Developer vanished with deposits. Millions lost!",
                "No social housing {location}. Homeless population growing daily."
            ],
            
            "unemployment_economy": [
                "Youth unemployment {location} at crisis levels. Government action needed! {urgency}",
                "Factory closure {location}. 200 workers jobless overnight. What now?",
                "Job scams targeting {location} residents. Fake recruitment agencies!",
                "Cost of living {location} unbearable. Unga price doubled. How do we survive?",
                "Market traders {location} being harassed by county officers. Corruption!",
                "No job opportunities for graduates in {location}. Brain drain happening.",
                "Small businesses {location} closing due to high taxes. Economy collapsing.",
                "Food prices {location} imepanda moo. Sukuma wiki now Ksh 50 per bunch!",
                "Salary delays {location} county workers. 3 months without pay! {urgency}",
                "Hustler fund not reaching {location} residents. System excluding us!"
            ],
            
            "child_welfare": [
                "Child abuse case {location} reported. System not protecting kids! {urgency}",
                "Street children increasing {location}. Where's social services?",
                "School dropout rate {location} rising. Poverty forcing kids to work.",
                "Child labor {location}. Kids working in quarries. Authorities must act! {urgency}",
                "Orphanage {location} overcrowded. Children sleeping on floor.",
                "No playgrounds {location}. Where should kids play safely?",
                "Child trafficking ring suspected {location}. Investigation needed! {urgency}",
                "Malnutrition among kids {location}. Families can't afford food. {urgency}",
                "Children walking 5km to school {location}. Need school buses!",
                "Teenage pregnancy crisis {location}. Youth programs needed urgently!"
            ],
            
            "gender_based_violence": [
                "GBV case {location} today. Victim needs help. Shelters? {urgency}",
                "Domestic violence increasing {location}. Women suffering in silence.",
                "Sexual assault {location} last night. Suspect still free. Police action? {urgency}",
                "FGM still happening {location}. Girls at risk. Intervention needed! {urgency}",
                "Rescue center {location} overwhelmed. More GBV survivors than capacity.",
                "Wife battery case {location}. Neighbors heard screams. Police came late.",
                "Early marriage {location}. 14-year-old forced to marry. Report this! {urgency}",
                "Harassment at {location} workplace. No HR action. Women need protection!",
                "GBV hotline not working {location}. Victims can't get help! {urgency}",
                "Support groups for survivors needed {location}. No counseling available."
            ],
            
            "environment": [
                "Deforestation {location}. Trees being cut illegally. KFS where are you?",
                "River pollution {location}. Factory dumping chemicals. NEMA act! {urgency}",
                "Air pollution {location} unbearable. Factory emissions causing health issues.",
                "Plastic menace {location}. Banned plastics still everywhere!",
                "Wetland invasion {location}. Construction on protected land. Stop this!",
                "Noise pollution from {location} bars. Residents can't sleep at night.",
                "Quarrying destroying {location} landscape. Environmental destruction!",
                "No trees in {location}. Urban heat unbearable. Plant trees initiative?",
                "E-waste dumping {location}. Toxic materials leaking. Health risk! {urgency}",
                "Wildlife conflict {location}. Elephants destroying crops. Compensation?"
            ],
            
            "corruption": [
                "Corruption at {location} county office. Bribes demanded for services!",
                "Ghost workers scandal {location}. Millions stolen from public funds!",
                "Tender irregularities {location} project. Investigation needed! {urgency}",
                "Land grabbing {location}. Public land being sold illegally!",
                "Kickbacks at {location} hospital. Suppliers colluding with officials!",
                "Bribery at {location} police station. Justice for sale!",
                "Fake documents being sold {location}. Corruption breeding crime!",
                "Procurement fraud {location} municipality. Inflated prices for projects!",
                "Embezzlement at {location} office. Where did our taxes go?",
                "Whistleblower threatened {location}. Expose corruption without fear!"
            ],
            
            "police_brutality": [
                "Police brutality {location} yesterday. Youth beaten for no reason! {urgency}",
                "Extortion by police {location}. Officers demanding bribes from matatus.",
                "Unlawful arrest {location}. Person detained without charge for 5 days!",
                "Police harassment at {location}. Stop and search turned violent.",
                "Excessive force used {location}. Peaceful protest dispersed with teargas!",
                "Police shooting {location}. Unarmed person killed. Justice needed! {urgency}",
                "Torture allegations {location} station. Suspects injured in custody.",
                "False charges {location}. Police planting evidence on innocent people!",
                "No accountability {location} police. Officers breaking law with impunity.",
                "Community demands police reforms {location}. End brutality now!"
            ],
            
            "drug_abuse": [
                "Drug problem {location} getting worse. Youth lives destroyed.",
                "Rehabilitation center {location} needed urgently. No facilities available!",
                "Drug peddlers {location} targeting schools. Kids at risk! {urgency}",
                "Alcoholism crisis {location}. Illegal brewers poisoning community.",
                "Bhang smoking openly {location}. Police turning blind eye!",
                "Prescription drug abuse {location}. Pharmacies selling without prescription.",
                "Youth rehab program {location} collapsed. No government support.",
                "Drug-related deaths {location} increasing. 3 ODs this week! {urgency}",
                "Parents {location} crying for help. Sons and daughters addicted.",
                "Needle exchange program needed {location}. HIV risk from sharing!"
            ],
            
            "mental_health": [
                "Mental health crisis {location}. No counseling services available!",
                "Suicide attempt {location} today. Where can people get help? {urgency}",
                "Depression levels {location} rising. Economic stress taking toll.",
                "No psychiatrist in {location}. Mental patients traveling 50km for care!",
                "Mental health stigma {location}. People suffering in silence.",
                "Psychiatric hospital {location} overcrowded. Inhumane conditions!",
                "Street families {location} need mental health support. System failing them.",
                "Post-trauma counseling needed {location} after fire. No services! {urgency}",
                "Burnout among {location} healthcare workers. Who cares for caregivers?",
                "Mental health awareness {location} needed. Community education crucial!"
            ],
            
            "disability_rights": [
                "No wheelchair access {location} building. Discrimination against PWDs!",
                "PWDs {location} excluded from job opportunities. This is injustice!",
                "Special needs school {location} closed. Where will kids go?",
                "Sign language interpreter shortage {location}. Deaf people isolated.",
                "Disability grants delayed {location}. People can't afford mobility aids!",
                "Sidewalks {location} not accessible. PWDs can't move independently.",
                "PWD abuse case {location}. Vulnerable people need protection! {urgency}",
                "No assistive devices {location} hospital. PWDs suffering unnecessarily.",
                "Discrimination at {location} workplace. PWD fired unfairly!",
                "Disability rights awareness {location} needed. End stigma now!"
            ]
        }
        
        # Urgency/emotional phrases (English, Sheng, Swahili)
        self.urgency_phrases = [
            "URGENT!", "Emergency!", "HARAKA!", "Critical!", "Hii ni serious!",
            "Immediate action needed!", "Lives at risk!", "Maisha iko hatarini!",
            "Please help!", "Tusaidie!", "Attention needed NOW!", "This is dangerous!",
            "Tutado?", "What's happening?", "Serikali msaada!", "Haki yetu!",
            "Enough is enough!", "Tumekataa!", "Justice needed!", "We demand action!",
            "Tuko rada!", "Shida mob!", "Hatuwezi vumilia!", "Action needed sasa!"
        ]
        
        # Expanded locations (30+ areas)
        self.locations = [
            "Kibera", "Eastleigh", "Westlands", "Karen", "Ngong Road", "CBD",
            "Kasarani", "Embakasi", "Langata", "Dagoretti", "Mathare", "Huruma",
            "Umoja", "Roysambu", "Ruaraka", "Pipeline", "Donholm", "Buruburu",
            "Kayole", "Zimmerman", "Githurai", "Kahawa West", "Mountain View",
            "Komarock", "Dandora", "Kariobangi", "Mukuru", "Kawangware",
            "Kangemi", "Madaraka", "South B", "South C", "Kilimani", "Lavington"
        ]
        
        # Expanded streets
        self.streets = [
            "Moi Avenue", "Kenyatta Avenue", "Uhuru Highway", "Waiyaki Way",
            "Thika Road", "Ngong Road", "Jogoo Road", "Outering Road",
            "Forest Road", "Limuru Road", "Kiambu Road", "Kangundo Road",
            "Mombasa Road", "Lang'ata Road", "Mbagathi Way", "Enterprise Road",
            "Industrial Area Road", "Haile Selassie Avenue", "Tom Mboya Street",
            "River Road", "Ronald Ngala Street", "Accra Road"
        ]
        
        # Platform weights
        self.platforms = ["Twitter", "Reddit", "Facebook"]
        self.platform_weights = [0.4, 0.35, 0.25]
        
        # Sentiment keywords for classification
        self.sentiment_keywords = {
            "positive": ["thanks", "solved", "better", "improved", "good", "happy", "asante", "poa", "sawa"],
            "negative": ["angry", "frustrated", "terrible", "worst", "useless", "disappointed", "hasira", "mbaya", "shida"],
            "urgent": ["urgent", "emergency", "critical", "immediate", "haraka", "danger", "hatari", "help", "tusaidie"]
        }
    
    def _detect_sentiment(self, text: str, is_urgent: bool) -> str:
        """Detect sentiment from text"""
        text_lower = text.lower()
        
        if is_urgent:
            return "urgent"
        
        # Check for negative keywords
        neg_count = sum(1 for word in self.sentiment_keywords["negative"] if word in text_lower)
        pos_count = sum(1 for word in self.sentiment_keywords["positive"] if word in text_lower)
        
        if neg_count > pos_count:
            return "negative"
        elif pos_count > neg_count:
            return "positive"
        else:
            return "neutral"
    
    def _generate_post_text(self, category: str) -> Tuple[str, bool, str]:
        """Generate post text with urgency and sentiment"""
        template = random.choice(self.issue_templates[category])
        
        # Replace placeholders
        text = template.replace("{location}", random.choice(self.locations))
        text = text.replace("{street}", random.choice(self.streets))
        text = text.replace("{days}", str(random.randint(2, 21)))
        text = text.replace("{time}", f"{random.randint(6, 120)} hours")
        
        # Detect urgency
        is_urgent = "{urgency}" in text
        if is_urgent:
            text = text.replace("{urgency}", random.choice(self.urgency_phrases))
        
        # Add hashtags (25% chance)
        if random.random() < 0.25:
            hashtags = [
                f"#{category.replace('_', '').title()}", "#Nairobi", "#Kenya",
                "#CommunityIssues", "#ServiceDelivery", "#FixOurCity",
                "#NairobiCounty", "#KOT", "#Accountability"
            ]
            text += " " + " ".join(random.sample(hashtags, random.randint(1, 3)))
        
        # Detect sentiment
        sentiment = self._detect_sentiment(text, is_urgent)
        
        return text, is_urgent, sentiment
    
    def _generate_engagement_metrics(self, platform: str, is_urgent: bool,
                                     sentiment: str, priority_boost: float = 1.0) -> Dict:
        """Generate realistic engagement with sentiment influence"""
        base_engagement = {
            "Twitter": {"retweet": (5, 150), "like": (10, 800)},
            "Reddit": {"score": (10, 1500), "comments": (5, 300)},
            "Facebook": {"share": (3, 120), "like": (15, 900), "comments": (5, 200)}
        }
        
        metrics = {}
        ranges = base_engagement[platform]
        
        # Multi-factor boost
        urgency_mult = 2.5 if is_urgent else 1.0
        sentiment_mult = 1.8 if sentiment == "urgent" else (1.3 if sentiment == "negative" else 1.0)
        priority_mult = priority_boost
        
        total_mult = urgency_mult * sentiment_mult * priority_mult
        
        for metric, (min_val, max_val) in ranges.items():
            boosted_max = int(max_val * total_mult)
            value = random.randint(min_val, boosted_max)
            metrics[metric] = value
        
        # Normalize format
        if platform == "Twitter":
            return {"retweet_count": metrics["retweet"], "favorite_count": metrics["like"]}
        elif platform == "Reddit":
            return {"retweet_count": metrics["score"], "favorite_count": metrics["comments"]}
        else:
            return {"retweet_count": metrics["share"], "favorite_count": metrics["like"]}
    
    def _generate_timestamp(self, days_back: int = 7) -> str:
        """Generate realistic timestamps"""
        now = datetime.now()
        days_ago = int(np.random.exponential(scale=days_back/3))
        days_ago = min(days_ago, days_back)
        
        # Working hours weighted
        hour_weights = [0.5] * 7 + [2.0] * 15 + [0.8] * 2
        hour = int(np.random.choice(range(24), p=np.array(hour_weights)/sum(hour_weights)))
        
        timestamp = now - timedelta(days=days_ago, hours=hour, minutes=random.randint(0, 59))
        return timestamp.isoformat()
    
    def generate_simulation_data(self, num_posts: int = 100,
                                 location: str = "Nairobi",
                                 days_back: int = 14) -> pd.DataFrame:
        """
        Generate comprehensive simulation data with specified number of posts
        """
        posts = []
        categories = list(self.issue_templates.keys())
        
        print(f"🚀 Generating {num_posts} posts across {len(categories)} categories...")
        
        for _ in range(num_posts):
            # Randomly select category for each post
            category = random.choice(categories)
            
            # Generate post
            text, is_urgent, sentiment = self._generate_post_text(category)
            platform = np.random.choice(self.platforms, p=self.platform_weights)
            
            # Priority boost for critical categories
            priority_boost = 1.8 if category in [
                "fire_emergency", "healthcare_facilities", "water_supply",
                "child_welfare", "gender_based_violence"
            ] else 1.0
            
            engagement = self._generate_engagement_metrics(
                platform, is_urgent, sentiment, priority_boost
            )
            timestamp = self._generate_timestamp(days_back)
            
            post = {
                "id": f"{platform.lower()}_{random.randint(100000, 999999)}_{category}",
                "text": text,
                "created_at": timestamp,
                "user": random.choice(self.usernames),
                "retweet_count": engagement["retweet_count"],
                "favorite_count": engagement["favorite_count"],
                "location": location,
                "source": platform,
                "category": category,
                "sentiment": sentiment,
                "is_urgent": is_urgent
            }
            posts.append(post)
        
        # Create DataFrame
        df = pd.DataFrame(posts)
        df['created_at'] = pd.to_datetime(df['created_at'])
        df = df.sort_values('created_at', ascending=False).reset_index(drop=True)
        df['created_at'] = df['created_at'].apply(lambda x: x.isoformat())
        
        print(f"✅ Generated {len(df)} total posts across {len(categories)} categories")
        return df
    
    def add_trending_issue(self, df: pd.DataFrame, category: str, 
                          num_related_posts: int = 20) -> pd.DataFrame:
        """
        Add a trending issue with multiple related posts
        (Simulates a viral community concern)
        """
        trending_location = random.choice(self.locations)
        base_timestamp = datetime.now() - timedelta(hours=random.randint(2, 24))
        
        trending_posts = []
        
        for i in range(num_related_posts):
            # Generate variations of the same issue
            text, is_urgent, sentiment = self._generate_post_text(category)
            # Force the same location for trending issue
            text = text.replace(random.choice(self.locations), trending_location)
            
            platform = np.random.choice(self.platforms, p=self.platform_weights)
            
            # Higher engagement for trending issues
            engagement = self._generate_engagement_metrics(platform, True, 3.0)
            
            # Timestamps clustered around base time
            timestamp = base_timestamp + timedelta(hours=random.randint(0, 12))
            
            post = {
                "id": f"{platform.lower()}_trending_{i}",
                "text": text,
                "created_at": timestamp.isoformat(),
                "user": random.choice(self.usernames),
                "retweet_count": engagement["retweet_count"],
                "favorite_count": engagement["favorite_count"],
                "location": trending_location,
                "source": platform,
                "category": category,
                "sentiment": sentiment,
                "is_urgent": is_urgent
            }
            
            trending_posts.append(post)
        
        # Combine with existing data
        trending_df = pd.DataFrame(trending_posts)
        combined_df = pd.concat([df, trending_df], ignore_index=True)
        
        # Sort by timestamp
        combined_df['created_at'] = pd.to_datetime(combined_df['created_at'])
        combined_df = combined_df.sort_values('created_at', ascending=False).reset_index(drop=True)
        combined_df['created_at'] = combined_df['created_at'].apply(lambda x: x.isoformat())
        
        return combined_df
    
    def save_simulation(self, df: pd.DataFrame, filename: str = None) -> str:
        """Save simulation data to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"simulation_data_{timestamp}.json"
        
        df.to_json(filename, orient="records", date_format="iso")
        print(f"✅ Simulation data saved to {filename}")
        return filename


# Example usage
if __name__ == "__main__":
    # Create simulator
    simulator = SocialMediaSimulator(seed=42)
    
    # Generate base simulation data
    print("Generating simulation data...")
    df = simulator.generate_simulation_data(num_posts=200, days_back=7)
    
    # Add a trending issue (e.g., water crisis)
    print("Adding trending issue...")
    df = simulator.add_trending_issue(df, category="water_supply", num_related_posts=25)
    
    # Display summary
    print(f"\n📊 Simulation Summary:")
    print(f"Total posts: {len(df)}")
    print(f"\nPosts by platform:")
    print(df['source'].value_counts())
    print(f"\nPosts by category:")
    print(df['category'].value_counts())
    print(f"\nSample posts:")
    print(df[['text', 'source', 'category']].head(5))
    
    # Save to file
    simulator.save_simulation(df)