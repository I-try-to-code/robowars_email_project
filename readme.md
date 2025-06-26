Absolutely, let's go step by step from scratch — **like you're doing this for the first time**.

---

## 🗂️ Step 1: Create Your Project Folder

1. Open a folder where you want to keep the project (e.g., `Documents` or `Desktop`)
2. Create a new folder named:
   **`robowars_email_project`**

---

## 📄 Step 2: Place These Files Inside the Folder

Your folder should contain:

| File Name                  | Description                                    |
| -------------------------- | ---------------------------------------------- |
| `send_emails.py`           | Main Python script you'll run                  |
| `contacts.csv`             | List of recipients (name, email, company)      |
| `robowars_brochure.pdf`    | Attachment 1                                   |
| `sponsorship_proposal.pdf` | Attachment 2                                   |
| `credentials.json`         | Gmail API credentials you download from Google |

---

## 🧠 Step 3: What Goes Inside `contacts.csv`

Create this file in Excel or any text editor, save it as `contacts.csv`:

```csv
recipient_name,email,company_name
Ravi Kumar,ravi@example.com,TechEdge
Sneha Rao,sneha@example.com,InnovateAI
```

---

## 🔑 Step 4: Get Gmail API Credentials

1. Go to: [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. Create a new project
3. Go to **APIs & Services → Library**

   * Search for **Gmail API** → Enable it
   * Make sure to set it to "External"
4. Go to **APIs & Services → Credentials**

   * Click **Create Credentials → OAuth client ID**
   * Choose **Desktop App**
   * Download the `credentials.json` file
5. Put this file in your project folder

---

## 🐍 Step 5: Install Required Python Libraries

Open terminal (CMD, PowerShell, or Mac Terminal), then:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

---

## 🧾 Step 6: Python Script (`send_emails.py`)

Edit this file according to the contents that you want to share. i wanted to add 2 more attatchments, so i have written the code as such. feel free to modify the code as per your needs.

## ▶️ Step 7: Run It!

In the terminal:

```bash
cd path/to/robowars_email_project
python send_emails.py
```

👉 On first run, a browser will open to authenticate your Gmail. Just log in and approve.

---

Let me know when you're ready, and I can help you test it on dummy emails.
