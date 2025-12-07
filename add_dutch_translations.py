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
    "Device Dashboard": "Apparaat Dashboard",
    "device(s) need attention (in system > 14 days).": "apparaat/apparaten hebben aandacht nodig (in systeem > 14 dagen).",
    "View reminders": "Bekijk herinneringen",
    "Search by Device ID, Customer Name, Phone, Device Type...": "Zoek op Apparaat ID, Klantnaam, Telefoon, Apparaattype...",
    "Search": "Zoeken",
    "All": "Alle",
    "Filter by Intaker:": "Filter op Intaker:",
    "All Intakers": "Alle Intakers",

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

    # Intake page
    "Device Intake": "Apparaat Intake",
    "New Device Intake": "Nieuwe Apparaat Intake",
    "Customer Name": "Klantnaam",
    "Phone Number": "Telefoonnummer",
    "Email Address": "E-mailadres",
    "Device Type": "Apparaattype",
    "Brand / Model": "Merk / Model",
    "Problem Description": "Probleembeschrijving",
    "Accessories": "Accessoires",
    "List any accessories brought with the device (charger, case, cables, etc.)": "Lijst eventuele accessoires bij het apparaat (oplader, hoesje, kabels, etc.)",
    "Register Device": "Apparaat Registreren",

    # Repair Station page
    "Search / Scan": "Zoeken / Scannen",
    "Device Information": "Apparaat Informatie",
    "Device ID:": "Apparaat ID:",
    "Status:": "Status:",
    "Intake Date:": "Intake Datum:",
    "Days in repair:": "Dagen in reparatie:",
    "Customer:": "Klant:",
    "Phone:": "Telefoon:",
    "Email:": "E-mail:",
    "Device Type:": "Apparaattype:",
    "Brand/Model:": "Merk/Model:",
    "Repairer:": "Reparateur:",
    "Date Finished:": "Datum Afgerond:",
    "Problem Description:": "Probleembeschrijving:",
    "ACCESSORIES:": "ACCESSOIRES:",
    "Repair Notes:": "Reparatie Notities:",
    "Update Status / Add Notes": "Status Bijwerken / Notities Toevoegen",
    "Print Label": "Label Afdrukken",
    "Not assigned": "Niet toegewezen",

    # Reminders page
    "Devices Needing Attention": "Apparaten die Aandacht Nodig Hebben",
    "Devices that have been in the system for more than 14 days and are not yet finished.": "Apparaten die langer dan 14 dagen in het systeem zitten en nog niet klaar zijn.",
    "No devices need attention at this time!": "Geen apparaten hebben op dit moment aandacht nodig!",
    "All devices are within the acceptable timeframe.": "Alle apparaten zijn binnen het acceptabele tijdsbestek.",
    "Back to Dashboard": "Terug naar Dashboard",

    # Detail page
    "Device Details": "Apparaat Details",
    "Customer Information": "Klantinformatie",
    "Name:": "Naam:",
    "Timeline": "Tijdlijn",
    "Finished Date:": "Afgerond Datum:",
    "Days in Repair:": "Dagen in Reparatie:",
    "Device Information": "Apparaat Informatie",
    "Repair Information": "Reparatie Informatie",
    "Repair Notes": "Reparatie Notities",
    "Update Device": "Apparaat Bijwerken",

    # Update page
    "Update Device": "Apparaat Bijwerken",
    "Device:": "Apparaat:",
    "Problem:": "Probleem:",
    "Accessories:": "Accessoires:",
    "Repairer Name": "Naam Reparateur",
    "Repair Notes / Solution": "Reparatie Notities / Oplossing",
    "Save Changes": "Wijzigingen Opslaan",

    # User Management
    "User Management": "Gebruikersbeheer",
    "Create New User": "Nieuwe Gebruiker Aanmaken",
    "Full Name": "Volledige Naam",
    "Email": "E-mail",
    "Role": "Rol",
    "Active": "Actief",
    "Inactive": "Inactief",
    "No users found.": "Geen gebruikers gevonden.",
    "First Name": "Voornaam",
    "Last Name": "Achternaam",
    "Confirm Password": "Bevestig Wachtwoord",
    "Active User": "Actieve Gebruiker",

    # User Delete Confirmation
    "Delete User": "Gebruiker Verwijderen",
    "Warning!": "Waarschuwing!",
    "Are you sure you want to delete this user?": "Weet je zeker dat je deze gebruiker wilt verwijderen?",
    "Username:": "Gebruikersnaam:",
    "Full Name:": "Volledige Naam:",
    "Role:": "Rol:",
    "This action cannot be undone. All data associated with this user will be affected.": "Deze actie kan niet ongedaan worden gemaakt. Alle gegevens die bij deze gebruiker horen worden beïnvloed.",

    # Print Label
    "Intake:": "Intake:",
    "Please attach this label to the device.": "Bevestig dit label aan het apparaat.",
    "Keep items together to prevent loss.": "Houd items bij elkaar om verlies te voorkomen.",
}

def add_translations():
    po_file_path = "locale/nl/LC_MESSAGES/django.po"

    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for english, dutch in translations.items():
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
