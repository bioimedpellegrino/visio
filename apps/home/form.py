from django import forms

class UserSelForm(forms.Form):
    face_recognition = forms.BooleanField(label='Face recognition', required=False)
    face_detection = forms.BooleanField(label='Face detection', required=False)
    face_emotion = forms.BooleanField(label='Emotion age gender', required=False)
    save_image = forms.BooleanField(label='Save images', required=False)
    sounds_on = forms.BooleanField(label='Sounds on', required=False)
    show_frame = forms.BooleanField(label="Show frame", required=False)