#!/usr/bin/env python3
"""
Script to add Dutch translations to the django.po file
"""

# Dutch translations for the application
translations = {
    # Navigation
    "Dashboard": "Dashboard",
    "New Intake": "Nieuwe Intake",
    "Repair Station": "Reparatiestation",
    "Reminders": "Herinneringen",
    "Users": "Gebruikers",
    "Admin": "Beheerder",
    "Operator": "Operator",
    "Logout": "Uitloggen",

    # Login page
    "Login": "Inloggen",
    "Device Management System": "Apparaatbeheersysteem",
    "Username": "Gebruikersnaam",
    "Enter your username": "Voer je gebruikersnaam in",
    "Password": "Wachtwoord",
    "Enter your password": "Voer je wachtwoord in",
    "Please login to access the system": "Log in om toegang te krijgen tot het systeem",

    # Dashboard page
    "Device Dashboard": "Dashboard",
    "device(s) need attention (in system > 14 days).": "apparaten nodig aandacht (> 14 dagen in systeem).",
    "View reminders": "Bekijk",
    "Search by Device ID, Customer Name, Phone, Device Type...": "Zoek op Apparaat ID, Naam, Telefoon, Type...",
    "Search": "Zoeken",
    "All": "Alle",
    "Filter by Intaker:": "Filter op:",
    "All Intakers": "Alle",

    # Table headers and common
    "Device ID": "Apparaat ID",
    "Customer": "Klant",
    "Device": "Apparaat",
    "Problem": "Probleem",
    "Status": "Status",
    "Intake Date": "Intake Datum",
    "Intaker": "Intaker",
    "Days": "Dagen",
    "Actions": "Acties",
    "View": "Bekijken",
    "No devices found.": "Geen apparaten gevonden.",
    "Phone": "Telefoon",
    "Yes": "Ja",
    "Cancel": "Annuleren",
    "Edit": "Bewerken",
    "Delete": "Verwijderen",
    "User": "Gebruiker",
    "Update": "Bijwerken",

    # Status choices
    "Open": "Open",
    "In Progress": "Bezig",
    "Repaired": "Opgelost",
    "Not Repaired": "Niet te repareren",
    "Free for Recycling": "Voor Recycling",

    # Intake page
    "Device Intake": "Intake",
    "New Device Intake": "Nieuwe Intake",
    "Customer Name": "Naam",
    "Phone Number": "Telefoon",
    "Email Address": "E-mail",
    "Device Type": "Type",
    "Brand / Model": "Merk / Model",
    "Problem Description": "Probleem",
    "Accessories": "Accessoires",
    "List any accessories brought with the device (charger, case, cables, etc.)": "Vermeld accessoires (oplader, hoesje, kabels, etc.)",
    "Register Device": "Registreren",

    # Repair Station page
    "Search / Scan": "Zoek / Scan",
    "Device Information": "Apparaat Info",
    "Device ID:": "ID:",
    "Status:": "Status:",
    "Intake Date:": "Intake:",
    "Days in repair:": "Dagen:",
    "Customer:": "Klant:",
    "Phone:": "Tel:",
    "Email:": "E-mail:",
    "Device Type:": "Type:",
    "Brand/Model:": "Merk/Model:",
    "Repairer:": "Reparateur:",
    "Date Finished:": "Afgerond:",
    "Problem Description:": "Probleem:",
    "ACCESSORIES:": "ACCESSOIRES:",
    "Repair Notes:": "Notities:",
    "Update Status / Add Notes": "Bijwerken / Notities",
    "Print Label": "Print Label",
    "Not assigned": "Niet toegewezen",

    # Reminders page
    "Devices Needing Attention": "Aandacht Nodig",
    "Devices that have been in the system for more than 14 days and are not yet finished.": "Apparaten die langer dan 14 dagen in het systeem zitten.",
    "No devices need attention at this time!": "Geen apparaten nodig aandacht!",
    "All devices are within the acceptable timeframe.": "Alle apparaten zijn op tijd.",
    "Back to Dashboard": "Terug",

    # Detail page
    "Device Details": "Details",
    "Customer Information": "Klant Info",
    "Name:": "Naam:",
    "Timeline": "Tijdlijn",
    "Finished Date:": "Afgerond:",
    "Days in Repair:": "Dagen:",
    "Device Information": "Apparaat Info",
    "Repair Information": "Reparatie Info",
    "Repair Notes": "Notities",
    "Update Device": "Bijwerken",

    # Update page
    "Update Device": "Bijwerken",
    "Device:": "Apparaat:",
    "Problem:": "Probleem:",
    "Accessories:": "Accessoires:",
    "Repairer Name": "Reparateur",
    "Repair Notes / Solution": "Notities / Oplossing",
    "Save Changes": "Opslaan",

    # User Management
    "User Management": "Gebruikers",
    "Create New User": "Nieuwe Gebruiker",
    "Full Name": "Naam",
    "Email": "E-mail",
    "Role": "Rol",
    "Active": "Actief",
    "Inactive": "Inactief",
    "No users found.": "Geen gebruikers.",
    "First Name": "Voornaam",
    "Last Name": "Achternaam",
    "Confirm Password": "Bevestig",
    "Active User": "Actief",

    # User Delete Confirmation
    "Delete User": "Verwijder Gebruiker",
    "Warning!": "Let op!",
    "Are you sure you want to delete this user?": "Weet je zeker dat je wilt verwijderen?",
    "Username:": "Naam:",
    "Full Name:": "Volledige Naam:",
    "Role:": "Rol:",
    "This action cannot be undone. All data associated with this user will be affected.": "Dit kan niet ongedaan gemaakt worden.",

    # Print Label
    "Intake:": "Intake:",
    "Please attach this label to the device.": "Bevestig dit label aan apparaat.",
    "Keep items together to prevent loss.": "Houd items bij elkaar.",
}

def add_translations():
    po_file_path = "locale/nl/LC_MESSAGES/django.po"

    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Sort by length (longest first) to avoid partial matches
    sorted_translations = sorted(translations.items(), key=lambda x: len(x[0]), reverse=True)

    for english, dutch in sorted_translations:
        # Find the msgid and replace empty msgstr
        pattern = f'msgid "{english}"\nmsgstr ""'
        replacement = f'msgid "{english}"\nmsgstr "{dutch}"'
        content = content.replace(pattern, replacement)

    # Update header info
    content = content.replace('#, fuzzy', '')
    content = content.replace('YEAR-MO-DA HO:MI+ZONE', '2025-12-07 00:00+0000')
    content = content.replace('FULL NAME <EMAIL@ADDRESS>', 'Repair Café Team')
    content = content.replace('Language: \\n', 'Language: nl\\n')

    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Dutch translations added to {po_file_path}")

if __name__ == "__main__":
    add_translations()
