# 🎉 Welcome to thanya2guide
Your one-stop destination to check exam results and stay updated with educational resources.

# 📘 thanya2guide

A result-checking website hosted on AWS S3 with backend powered by AWS Lambda and API Gateway.

---

## 📁 Folder Structure

```
thanya2guide/
├── ui/                      # Frontend code
│   ├── index.html           # Home page
│   ├── results.html         # Results checking page
│   ├── contact-us.html      # Contact page
│   ├── footer.html          # Shared footer (included via JS)
│   └── assets/              # Static assets
│       ├── css/
│       ├── js/
│       └── images/

├── api/                     # Backend Lambda function
│   ├── lambda_function.py   # Python Lambda code
│   └── lambda.zip           # Zipped Lambda function for deployment

├── infra/                   # Infra configs/scripts
│   ├── s3_bucket_policy.json  # S3 bucket policy for public read-only access
│   └── deploy_commands.sh     # Deployment helper script



├── data/                   # Actual results data in .json or .txt
│   ├── 2025
│       ├── tgcet_5th_class_results.json  # S3 bucket policy for public read-only access
```

---

## 🚀 Deployment Instructions

### 1. Upload UI to AWS S3

Make sure your S3 bucket is set up for static website hosting.

```bash
aws s3 sync ui/ s3://thanya2guide/
```

Your site will be available at:
🌐 **http://thanya2guide.s3-website.ap-south-1.amazonaws.com**

---

### 2. Deploy Lambda Function

From the `api/` directory:

```bash
zip -r lambda.zip lambda_function.py results.json
```

Upload `lambda.zip` to your Lambda function via AWS Console or AWS CLI.

Ensure:
- **Runtime** is Python 3.12
- **Handler** is `lambda_function.lambda_handler`
- Lambda has permission to read from your S3 bucket (if needed)

---

### 3. Setup API Gateway (REST API)

- Create a new REST API
- Enable **CORS** for `/check` POST method
- Integrate with your Lambda function
- Deploy to a stage, e.g., `/prod`

Your API endpoint will look like:
🔗 `https://your-api-id.execute-api.ap-south-1.amazonaws.com/prod/check`

---

## 🌟 Features

- Fast student result search using a JSON file (dict with hallticket as key)
- Results displayed neatly using TailwindCSS
- Graceful fallback for not-found students
- Loading indicator during search
- Beautiful layout and shared footer

---

## 📬 Social Links (in footer)

- 📺 [YouTube Channel](https://www.youtube.com/watch?v=XG_Y7pq82cc)
- 📸 [Instagram](https://instagram.com/thanya2guide)
- 📢 [Telegram](https://t.me/thanya2_guide)
- 💬 [WhatsApp Channel](https://whatsapp.com/channel/0029VaAbo7b4NVisLv9yRM44)
- 📝 [Blog](https://thanya2guide.blogspot.com)
- 🌐 [Beacons](https://beacons.ai/signup?c=thanya2guide)

---

## 🛠 Tech Stack

- **Frontend:** HTML + TailwindCSS + Vanilla JS
- **Backend:** Python (AWS Lambda)
- **Infra:** AWS S3, Lambda, API Gateway

---

## 📌 Notes

- Footer is reused across all pages via JavaScript injection of `footer.html`
- Results JSON should have format:

```json
{
  "1234567890": {
    "Hall_Ticket_Number": "1234567890",
    "Student_Name": "John Doe",
    "School": "XYZ High School"
    // ...
  }
}
```