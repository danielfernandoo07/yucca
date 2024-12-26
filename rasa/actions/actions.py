import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionFetchKnowledgeBase(Action):
    def name(self) -> Text:
        return "action_fetch_knowledge_base"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Path to your JSON file
        kb_path = "data/kb.json"

        # Load the JSON file
        try:
            with open(kb_path, "r", encoding="utf-8") as file:
                knowledge_base = json.load(file)
        except FileNotFoundError:
            dispatcher.utter_message(text="Basis pengetahuan tidak tersedia.")
            return []

        # Retrieve intent and entities
        intent = tracker.get_intent_of_latest_message()
        program_studi = tracker.get_slot("program_studi")
        fakultas = tracker.get_slot("fakultas")

        # Default response
        response = "Maaf, saya tidak memiliki informasi untuk pertanyaan tersebut."

        try:
            # Handle specific intents dynamically from the knowledge base
            if intent == "ask_about_university":
                university = knowledge_base.get("universitas", {})
                response = (
                    f"Universitas Ciputra berlokasi di {university.get('lokasi', 'lokasi tidak tersedia')}.\n"
                    f"Website: {university.get('website', 'website tidak tersedia')}.\n"
                    f"Kontak: {university.get('contact', {}).get('phone', 'kontak tidak tersedia')}."
                )

            elif intent == "ask_about_faculties":
                faculties = [f"- {f['nama']}" for f in knowledge_base.get("fakultas", [])]
                response = "Berikut adalah fakultas yang tersedia:\n" + "\n".join(faculties)

            elif intent == "ask_about_tuition":
                tuition_info = knowledge_base.get("program_studi", [])
                if program_studi:
                    program = next((p for p in tuition_info if p["nama"].lower() == program_studi.lower()), None)
                    if program:
                        response = (
                            f"Biaya untuk program studi {program['nama']}:\n"
                            f"- DPP: {program['biaya']['dpp']}\n"
                            f"- SPP Reguler: {program['biaya']['spp_reguler']}\n"
                            f"- Total: {program['biaya']['total']}"
                        )
                    else:
                        response = f"Maaf, saya tidak menemukan informasi biaya untuk program studi {program_studi}."
                else:
                    response = "Maaf, saya tidak tahu program studi mana yang Anda maksud. Bisa sebutkan nama jurusannya?"

            elif intent == "ask_about_registration":
                registration_info = knowledge_base.get("pendaftaran", [{}])[0].get("tata_cara_pendaftaran", [])
                if registration_info:
                    response = "Berikut adalah langkah-langkah pendaftaran:\n" + "\n".join(
                        [f"- {step['deskripsi']}" for step in registration_info]
                    )
                else:
                    response = "Maaf, saya tidak menemukan informasi pendaftaran."

            elif intent == "ask_about_scholarship":
                scholarships = knowledge_base.get("beasiswa", [])
                if scholarships:
                    response = "Universitas Ciputra menyediakan beasiswa berikut:\n" + "\n".join(
                        [f"- {scholarship['nama']}: {scholarship['deskripsi']}" for scholarship in scholarships]
                    )
                else:
                    response = "Maaf, informasi beasiswa tidak tersedia saat ini."

            elif intent == "ask_about_yucca":
                response = (
                    "Yucca adalah maskot Universitas Ciputra yang melambangkan nilai integritas, profesionalisme, dan kewirausahaan."
                )

            elif intent == "ask_about_life_on_campus":
                campus_life = knowledge_base.get("kehidupan_kampus", [])
                if campus_life:
                    response = "Kehidupan kampus di Universitas Ciputra mencakup:\n" + "\n".join(
                        [f"- {activity}" for activity in campus_life]
                    )
                else:
                    response = "Maaf, saya tidak memiliki informasi tentang kehidupan kampus."

            elif intent == "ask_about_contact_information":
                contact = knowledge_base.get("universitas", {}).get("contact", {})
                response = (
                    f"Informasi kontak Universitas Ciputra:\n"
                    f"Telepon: {contact.get('phone', 'tidak tersedia')}\n"
                    f"Email: {contact.get('email', 'tidak tersedia')}."
                )

            elif intent == "ask_about_academic_process":
                academic_process = knowledge_base.get("proses_akademik", [])
                if academic_process:
                    response = "Berikut adalah informasi tentang proses akademik:\n" + "\n".join(
                        [f"- {item}" for item in academic_process]
                    )
                else:
                    response = "Maaf, informasi tentang proses akademik tidak tersedia."

            elif intent == "ask_about_graduation_and_career":
                graduation_info = knowledge_base.get("karir", [])
                if graduation_info:
                    response = "Berikut adalah informasi tentang karir dan lulusan:\n" + "\n".join(
                        [f"- {item}" for item in graduation_info]
                    )
                else:
                    response = "Maaf, informasi tentang karir dan lulusan tidak tersedia."

            elif intent == "ask_about_university_policy":
                policies = knowledge_base.get("kebijakan", [])
                if policies:
                    response = "Berikut adalah kebijakan Universitas Ciputra:\n" + "\n".join(
                        [f"- {policy}" for policy in policies]
                    )
                else:
                    response = "Maaf, informasi kebijakan tidak tersedia."

            else:
                response = "Maaf, saya tidak memiliki informasi untuk pertanyaan tersebut."

        except Exception as e:
            response = f"Terjadi kesalahan: {str(e)}"

        # Send response
        dispatcher.utter_message(text=response)
        return []
