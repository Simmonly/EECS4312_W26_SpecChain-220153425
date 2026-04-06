# Medito – Manual Software Specification
## Pipeline: Manual | Source: personas/personas_manual.json

---

# Requirement ID: FR1
- **Description:** The system shall provide full access to all meditation content without requiring any payment, subscription, or donation.
- **Source Persona:** P1 – The Grateful Free User
- **Traceability:** Derived from review group G1
- **Acceptance Criteria:** Given a user opens the app for the first time, when they browse the content library, then all meditation sessions and courses shall be accessible without any payment prompt or locked content indicator.

---

# Requirement ID: FR2
- **Description:** The system shall never display advertisements during or between meditation sessions.
- **Source Persona:** P1 – The Grateful Free User
- **Traceability:** Derived from review group G1
- **Acceptance Criteria:** Given a user is in an active meditation session or navigating between sessions, when any screen transition occurs, then no advertisement of any kind shall be displayed.

---

# Requirement ID: FR3
- **Description:** The system shall provide a clearly visible option to skip or dismiss any donation prompt without restricting access to content.
- **Source Persona:** P2 – The Confused First-Timer
- **Traceability:** Derived from review group G2
- **Acceptance Criteria:** Given a donation prompt appears during onboarding or app use, when the user views the prompt, then a skip or dismiss button shall be visible without scrolling, and dismissing it shall grant full access to the app.

---

# Requirement ID: FR4
- **Description:** The system shall not display a recurring donation nag screen to users who have already donated.
- **Source Persona:** P2 – The Confused First-Timer
- **Traceability:** Derived from review group G2
- **Acceptance Criteria:** Given a user has completed a donation, when they reopen the app or navigate between screens, then the donation prompt shall not reappear in that session or future sessions.

---

# Requirement ID: FR5
- **Description:** The system shall continue playing audio when the device screen is turned off or locked.
- **Source Persona:** P3 – The Frustrated Returning User
- **Traceability:** Derived from review group G3
- **Acceptance Criteria:** Given a user has started a meditation session, when the device screen turns off or locks, then the audio shall continue playing uninterrupted until the session ends or the user manually pauses it.

---

# Requirement ID: FR6
- **Description:** The system shall sync user progress, streaks, and completed sessions reliably across all devices linked to the same account.
- **Source Persona:** P3 – The Frustrated Returning User
- **Traceability:** Derived from review group G3
- **Acceptance Criteria:** Given a user has completed sessions on one device, when they log into the same account on a different device, then their streak count, course progress, and session history shall be identical across both devices within 60 seconds of login.

---

# Requirement ID: FR7
- **Description:** The system shall mark a meditation session as complete when the user exits within the final 10 seconds of the session audio.
- **Source Persona:** P3 – The Frustrated Returning User
- **Traceability:** Derived from review group G3
- **Acceptance Criteria:** Given a user exits a session within the last 10 seconds of audio playback, when the system checks session completion, then the session shall be recorded as completed and counted toward the user's streak and progress.

---

# Requirement ID: FR8
- **Description:** The system shall allow users to queue multiple meditation sessions to play consecutively without requiring manual interaction between sessions.
- **Source Persona:** P4 – The Wellness Seeker
- **Traceability:** Derived from review group G4
- **Acceptance Criteria:** Given a user has built a queue of two or more meditation sessions, when the first session ends, then the next session in the queue shall begin playing automatically without requiring the user to unlock their phone or interact with the app.

---

# Requirement ID: FR9
- **Description:** The system shall allow users to download meditation sessions for offline playback.
- **Source Persona:** P5 – The Beginner on a Journey
- **Traceability:** Derived from review group G5
- **Acceptance Criteria:** Given a user is viewing a meditation session page, when they tap the download button, then the session shall be saved locally and shall be playable without an internet connection, with the download button clearly visible on the session screen.

---

# Requirement ID: FR10
- **Description:** The system shall provide a structured beginner course that guides new users through meditation fundamentals in a sequential, clearly labelled progression.
- **Source Persona:** P5 – The Beginner on a Journey
- **Traceability:** Derived from review group G5
- **Acceptance Criteria:** Given a first-time user opens the app, when they navigate to the courses section, then a beginner course shall be prominently displayed, with sessions listed in order and each session labelled with its sequence number and estimated duration.

---

# Requirement ID: FR11
- **Description:** The system shall allow users to manually log a meditation session completed outside the app so that their streak is not broken.
- **Source Persona:** P3 – The Frustrated Returning User
- **Traceability:** Derived from review group G3
- **Acceptance Criteria:** Given a user meditated without using the app, when they open the app and navigate to their streak settings, then they shall be able to manually add a session for a past date, and the streak shall update to reflect that entry.

---

# Requirement ID: FR12
- **Description:** The system shall provide an option to disable in-app swipe gestures that conflict with the device's native navigation gestures.
- **Source Persona:** P3 – The Frustrated Returning User
- **Traceability:** Derived from review group G3
- **Acceptance Criteria:** Given a user navigates to app settings, when they locate the gesture controls option, then they shall be able to disable swipe gestures within the app, and the device's native navigation gestures shall function without interference after doing so.
