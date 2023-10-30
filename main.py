import google.generativeai as genai
import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configure Google Generative AI with your API key
genai.configure(api_key="AIzaSyC0zr-PvWo_OlzqEFro-pzyV6zFqEZ41OI")

# Define your email and bot configurations
EMAIL_ADDRESS = "ceo.etherealai@gmail.com"
EMAIL_PASSWORD = "kxnk rnni jjli jzjx"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

# Create a function to send an email
def send_email(subject, message, to_email):
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:

        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        msg = f"Subject: {subject}\n\n{message}"
        msg = msg.encode("utf-8")

        server.sendmail(EMAIL_ADDRESS, to_email, msg)

# Create a function to fetch and process emails
def process_emails():
    with imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT) as mail:
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select("inbox")
        status, email_ids = mail.search(None, "UNSEEN")  # Fetch unread emails

        if status == "OK":
            email_id_list = email_ids[0].split()
            for email_id in email_id_list:
                status, email_data = mail.fetch(email_id, "(RFC822)")
                if status == "OK":
                    raw_email = email_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    sender_email = msg["From"]
                    email_subject = msg["Subject"]

                    # Extract the email query from the email body
                    email_query = msg.get_payload(decode=True).decode()

                    # Define context and examples for the Generative AI
                    context = "Given an email, write a reply email in a concise, professional manner. Your name is 'Nebula AI \n Customer Service'. Always end all emails with '\nThis email was written by our AI Agent. If it doesn't make sense, please let us know so we can improve it further.' Always use numbers as bullets instead of asterisks."
                    examples = [
                        [
                            "What is your company information?",
                            "Dear [name],\n\n Ethereal is an AI automation and integration agency that helps unlock the full potential of businesses by automating routine tasks, reducing costs, and enhancing productivity. With AI Process Automation, Improve the customer experience with Custom AI Chatbots, and other incredible things using AI, machine learning, and computer vision. You can focus on what truly matters—innovation, growth, and delivering exceptional value to your customers. we are the architects of innovation, the creators of efficiency, and the champions of a future where artificial intelligence empowers and elevates the capabilities of businesses and individuals alike. We are more than just a technology company; we are the catalysts of transformation in the digital era."
                        ],
                        [
                            "What are your services?",
                            "Dear [name],\n\n1. AI Process Automation: \nUnlocking Efficiency Through Intelligent Automation \nIn today's fast-paced business landscape, efficiency is paramount. AI Process Automation is the key to streamlining your operations, reducing manual efforts, and achieving greater productivity. Our AI Automation Agency specializes in harnessing the power of artificial intelligence to revolutionize the way you work. \nHow AI Process Automation Can Benefit Your Business: \nStreamlined Workflows: We analyze your existing processes and identify repetitive and time-consuming tasks. Our experts then design and implement AI-powered solutions to automate these processes, reducing errors and increasing efficiency. \nEnhanced Customer Support: Say goodbye to long wait times and frustrated customers. Our AI chatbots and virtual assistants can handle customer inquiries, provide instant support, and even assist with transactions, ensuring your customers receive prompt and consistent service. \nData Accuracy: Manual data entry is prone to errors. With AI automation, you can achieve near-perfect accuracy in data processing. Whether it's invoice processing, data extraction, or inventory management, we can automate it with precision. \nCost Savings: By automating repetitive tasks, you can significantly reduce labor costs and free up your workforce to focus on more value-added activities. AI Process Automation is a cost-effective solution for businesses of all sizes. \nScalability: Our AI automation solutions are designed to grow with your business. As your needs evolve, we can easily scale up the automation processes to accommodate increased workloads. \nOur Approach to AI Process Automation: \nCustom Solutions: We understand that each business is unique, and there is no one-size-fits-all solution. Our team works closely with you to understand your specific requirements and tailors AI automation solutions to meet your objectives. \nSeamless Integration: We ensure that the AI automation seamlessly integrates with your existing IT infrastructure and software, minimizing disruptions to your operations. \nContinuous Improvement: AI automation is not a one-time endeavor. We constantly monitor and refine the automated processes to adapt to changing business needs and technology advancements. \nData Security: We prioritize the security of your data. Our AI automation solutions are designed with robust data encryption and access controls to protect your sensitive information. \nRealize the Potential of AI Process Automation. \nLet us help you unlock the full potential of your business by automating routine tasks, reducing costs, and enhancing productivity. With AI Process Automation, you can focus on what truly matters—innovation, growth, and delivering exceptional value to your customers. \nContact us today to explore how AI automation can transform your business processes and drive your organization toward a future of efficiency and excellence."
                        ],
                        [
                            "What are your prices?",
                            "Dear [name],\n\n Prices can vary depending on your needs and we can do for you. Let's have a talk to learn more about your business and give you the best support needed. It can be as low as 100 dollars per month!"
                        ],
                        [
                            "What are your contact information?",
                            "Dear [name],\n\n Let's have a talk to learn more about what you need and give you the best support needed. \nPhone: +201129737208 \nEmail:ceo.etherealai@gmail.com \nWebsite: https://etherealai.tech"
                        ]
                    ]

                    # Use Google Generative AI to generate a response
                    response = genai.chat(
                        context=context,
                        examples=examples,
                        messages=[email_query]
                    )

                    # Extract the response from the Generative AI
                    ai_response = response.last

                    # Send the AI-generated response as an email
                    send_email(f"Re: {email_subject}", ai_response, sender_email)
                    print(f"Replied to {sender_email} with: {ai_response}")

if __name__ == "__main__":
    process_emails()