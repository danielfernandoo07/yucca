import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Dict, Text, Any, List


def load_knowledge_base() -> Dict:
    """Load knowledge base from JSON file."""
    kb_path = "data/kb.json"
    try:
        with open(kb_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


class ActionFetchKnowledgeBase(Action):
    def name(self) -> Text:
        return "action_fetch_knowledge_base"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        knowledge_base = load_knowledge_base()

        # Get the latest user intent
        intent = tracker.latest_message["intent"]["name"]

        if intent == "ask_about_all_faculties":
            faculties = knowledge_base.get("fakultas", [])
            response = "Fakultas yang tersedia:\n" + "\n".join(
                [f"- {faculty['nama']}" for faculty in faculties]
            )
            dispatcher.utter_message(text=response)

        elif intent == "ask_about_registration":
            registration_info = knowledge_base.get("pendaftaran", [])
            response = "Informasi Pendaftaran:\n" + "\n".join(
                [f"- {info}" for info in registration_info[0]["informasi_pendaftaran"]]
            )
            dispatcher.utter_message(text=response)

        else:
            dispatcher.utter_message(
                text="Maaf, saya tidak dapat menemukan informasi tersebut."
            )

        return []

class ActionFetchValueLambang(Action):
    def name(self) -> Text:
        return "action_fetch_value_lambang"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # Muat knowledge base
        knowledge_base = load_knowledge_base()

        # Ambil entitas 'value' dari tracker
        entity = tracker.get_slot("value")

        # Ambil informasi nilai dari knowledge base
        values = knowledge_base.get("yucca_identity", {}).get("character", {}).get("values", {})
        response = values.get(entity.lower(), f"Maaf, saya tidak memiliki informasi tentang nilai {entity}.")

        dispatcher.utter_message(text=response)
        return []

class ActionFetchMission(Action):
    def name(self) -> Text:
        return "action_fetch_mission"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # Muat knowledge base
        knowledge_base = load_knowledge_base()

        # Ambil informasi misi dari knowledge base
        mission = (
            knowledge_base.get("yucca_identity", {})
            .get("koneksi_dengan_uc", {})
            .get("misi", "Maaf, saya tidak memiliki informasi tentang misi Yucca.")
        )

        dispatcher.utter_message(text=mission)
        return []


class ActionProvideUniversityContact(Action):
    def name(self) -> Text:
        return "action_provide_university_contact"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        knowledge_base = load_knowledge_base()
        contact_info = knowledge_base.get("universitas", {}).get("contact", {})

        # Format respons kontak
        phone = contact_info.get("phone", "Nomor telepon tidak tersedia.")
        instagram = contact_info.get("instagram", "Instagram tidak tersedia.")
        facebook = contact_info.get("facebook", "Facebook tidak tersedia.")
        tiktok = contact_info.get("tiktok", "TikTok tidak tersedia.")
        youtube = contact_info.get("youtube", "YouTube tidak tersedia.")

        response = (
            f"Anda dapat menghubungi Universitas Ciputra melalui:\n"
            f"- Telepon: {phone}\n"
            f"- Instagram: @{instagram}\n"
            f"- Facebook: {facebook}\n"
            f"- TikTok: {tiktok}\n"
            f"- YouTube: {youtube}"
        )

        dispatcher.utter_message(text=response)
        return []


class ActionProvideSocialMedia(Action):
    def name(self) -> Text:
        return "action_provide_social_media"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        knowledge_base = load_knowledge_base()
        social_media_accounts = knowledge_base.get("universitas", {}).get("contact", {})

        # Ambil entitas platform
        platform = tracker.get_slot("platform")

        # Cek apakah platform ada di daftar sosial media
        if platform and platform.lower() in social_media_accounts:
            account = social_media_accounts[platform.lower()]
            response = (
                f"Akun {platform.capitalize()} Universitas Ciputra adalah: {account}."
            )
        else:
            # Respons default jika platform tidak ditemukan
            response = f"Maaf, saya tidak memiliki informasi tentang {platform}. Silakan tanyakan sosial media lain."

        dispatcher.utter_message(text=response)
        return []


class ActionProvideUniversityInfo(Action):
    def name(self) -> str:
        return "action_provide_university_info"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, List],
    ) -> List[Dict]:
        # Muat knowledge base dari JSON
        knowledge_base = load_knowledge_base()

        # Ambil informasi universitas dari knowledge base
        university_info = knowledge_base.get("universitas", {})

        # Mendapatkan intent terbaru
        intent = tracker.get_intent_of_latest_message()

        # Memilih respons berdasarkan intent
        if intent == "ask_about_university_address":
            address = university_info.get("address", "Alamat tidak tersedia.")
            response = f"Alamat Universitas Ciputra adalah: {address}."
        elif intent == "ask_about_university_website":
            website = university_info.get("website", "Website tidak tersedia.")
            response = f"Website resmi Universitas Ciputra adalah: {website}."
        elif intent == "ask_about_university_phone":
            phone = university_info.get("phone", "Nomor telepon tidak tersedia.")
            response = f"Nomor telepon Universitas Ciputra adalah: {phone}."
        else:
            response = "Maaf, saya tidak memiliki informasi tentang hal itu."

        # Kirim respons ke pengguna
        dispatcher.utter_message(text=response)
        return []


class ActionProvideFacultyDetails(Action):
    def name(self) -> Text:
        return "action_provide_faculty_details"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        knowledge_base = load_knowledge_base()
        faculties = knowledge_base.get("fakultas", [])

        # Ambil kode fakultas dari slot
        kode_fakultas = tracker.get_slot("kode_fakultas")

        if kode_fakultas:
            # Cari fakultas berdasarkan kode
            faculty = next(
                (f for f in faculties if f["kode"].lower() == kode_fakultas.lower()), None
            )
            if faculty:
                response = (
                    f"Fakultas dengan kode {faculty['kode']} adalah {faculty['nama']} "
                    f"(dikenal juga sebagai {faculty['nama_inggris']})."
                )
            else:
                response = f"Maaf, saya tidak dapat menemukan fakultas dengan kode {kode_fakultas}."
        else:
            response = (
                "Maaf, saya tidak mendeteksi kode fakultas. Silakan coba lagi dengan memberikan kode fakultas yang valid."
            )

        dispatcher.utter_message(text=response)
        return []
    
class ActionProvideAllPrograms(Action):
    def name(self) -> Text:
        return "action_provide_all_programs"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        knowledge_base = load_knowledge_base()
        programs = knowledge_base.get("program_studi", [])
        response = "Universitas Ciputra memiliki program studi berikut:\n"
        response += "\n".join([f"- {program['nama']} ({program['kode']})" for program in programs])
        dispatcher.utter_message(text=response)
        return []


class ActionProvideProgramDetails(Action):
    def name(self) -> Text:
        return "action_provide_program_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        kb = load_knowledge_base()
        kode_program_studi = tracker.get_slot("kode_program_studi")
        program = next((p for p in kb.get("program_studi", []) if p["kode"].lower() == kode_program_studi.lower()), None)

        if program:
            faculty_name = program.get("kode_fakultas", "Fakultas tidak ditemukan")
            response = (
                f"Program studi {program['nama']} (kode: {program['kode']}) adalah bagian dari fakultas {faculty_name}."
            )
        else:
            response = "Maaf, saya tidak dapat menemukan informasi tentang program studi tersebut."

        dispatcher.utter_message(text=response)
        return []

class ActionProvideFacultyPrograms(Action):
    def name(self) -> Text:
        return "action_provide_faculty_programs"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        kb = load_knowledge_base()
        kode_fakultas = tracker.get_slot("kode_fakultas")
        programs = [p for p in kb.get("program_studi", []) if p["kode_fakultas"].lower() == kode_fakultas.lower()]

        if programs:
            response = (
                f"Program studi di fakultas {kode_fakultas}:\n" +
                "\n".join([f"- {p['nama']} ({p['kode']})" for p in programs])
            )
        else:
            response = "Maaf, saya tidak dapat menemukan program studi di fakultas tersebut."

        dispatcher.utter_message(text=response)
        return []

class ActionProvideProgramRequirements(Action):
    def name(self) -> Text:
        return "action_provide_program_requirements"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        kb = load_knowledge_base()
        kode_program_studi = tracker.get_slot("kode_program_studi")
        program = next((p for p in kb.get("program_studi", []) if p["kode"].lower() == kode_program_studi.lower()), None)

        if program and "persyaratan" in program:
            response = (
                f"Persyaratan untuk {program['nama']}:\n" +
                "\n".join([f"- {req['jenis']}: {req['detail']}" for req in program["persyaratan"]])
            )
        else:
            response = "Maaf, saya tidak dapat menemukan informasi persyaratan untuk program studi tersebut."

        dispatcher.utter_message(text=response)
        return []

class ActionProvideProgramSelection(Action):
    def name(self) -> Text:
        return "action_provide_program_selection"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        kb = load_knowledge_base()
        kode_program_studi = tracker.get_slot("kode_program_studi")
        program = next((p for p in kb.get("program_studi", []) if p["kode"].lower() == kode_program_studi.lower()), None)

        if program and "seleksi_khusus" in program:
            response = (
                f"Seleksi khusus untuk {program['nama']}:\n" +
                "\n".join([f"- {sel['jenis']}: {sel['contoh_soal']}" for sel in program["seleksi_khusus"]])
            )
        else:
            response = "Maaf, saya tidak dapat menemukan informasi seleksi untuk program studi tersebut."

        dispatcher.utter_message(text=response)
        return []

class ActionProvideProgramFees(Action):
    def name(self) -> Text:
        return "action_provide_program_fees"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        kb = load_knowledge_base()
        kode_program_studi = tracker.get_slot("kode_program_studi")
        program = next((p for p in kb.get("program_studi", []) if p["kode"].lower() == kode_program_studi.lower()), None)

        if program and "biaya" in program:
            biaya = program["biaya"]
            response = (
                f"Biaya untuk {program['nama']}:\n"
                f"- DPP: {biaya.get('dpp', 'N/A')}\n"
                f"- SPP Kerjasama: {biaya.get('spp_kerjasama', 'N/A')}\n"
                f"- SPP Reguler: {biaya.get('spp_reguler', 'N/A')}\n"
                f"- SKS: {biaya.get('sks', 'N/A')}\n"
                f"- ORI: {biaya.get('ori', 'N/A')}\n"
                f"Total: {biaya.get('total', 'N/A')}"
            )
        else:
            response = "Maaf, saya tidak dapat menemukan informasi biaya untuk program studi tersebut."

        dispatcher.utter_message(text=response)
        return []