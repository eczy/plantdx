# plant-dx

##### demo: https://streamable.com/6mtiz

## Inspiration
Elia: Cacao, one of the many exports of the Dominican Republic, has been in my family for many generations. Passed down from my great-grandfather to my mother, it is important - both for agricultural sustainability and family consciousness - that we do what we can to make sure this land continues to survive through time. Motivated by the many agricultural challenges that surround the cacao community, we leverage computer vision to help farmers immediately identify and treat ongoing plant illnesses that result in crop yield reduction for the harvest year..

Evan: I have some background in computer vision and was motivated by Elia’s story to apply this skill in the realm of sustainability. I also wanted to explore edge machine learning using PyTorch, and this seemed like an obvious fit. Also, Elia called her mom to confirm that this is a useful idea.

## What it does
We present a mindful and accessible solution to treating plant diseases by giving the farmer the power of edge machine learning. The app and model, run entirely on the phone, allows a farmer to take a photo of the suspected plant they think is ill, and the model will predict its disease status. Using an in-house API, we also recommend relevant plant treatments that help the farmer gain more insight on how to approach the situation.

## How we built it
Conscious of financial costs to farmers, we wanted to build an app that was easy to use and cost-effective in terms of data usage. Recognizing that many 3rd-world countries use pay-as-you-go data plans and that internet availability isn’t always available/reliable, relying on the backend for disease identification simply won’t work. Because of this, we decided to build an app that has the machine learning inference baked into it. This means that the image doesn’t need to be sent to the backend to be identified, and the farmer can use this functionality fully offline. If the farmer does have internet access, our API also can recommend treatment for any identified plant diseases when identified.

## Challenges we ran into
Connecting Atlas Mongo DB to Google Cloud Functions
Pytorch for mobile is still in beta, so incorporating our model into the iOS app was somewhat difficult
Accomplishments that we're proud of
We’re proud that our proof of concept works! Our edge machine learning model achieves very good performance (~0.95 average precision) and works flawlessly on iOS, and we were able to successfully build a simple serverless backend using GCP and MongoDB Atlas.

## What we learned
Elia learned back-end (how to make an API, infrastructure, docker)! Evan learned how to deploy machine learning models to iOS as an edge device.

## What's next for PlantDx
Model refinements (more data, better quantization, approximate region identification)
Code cleanup
Backend hardening
Add option for realtime video rather than singular images
(Re)Deployment :D



Website: devpost: https://devpost.com/software/plantdx



