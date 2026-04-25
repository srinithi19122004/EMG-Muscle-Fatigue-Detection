import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import warnings
warnings.filterwarnings('ignore')

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay

df = pd.read_excel(r"C:\Users\acer\Desktop\EMG-ML-PROJECT\emg_combined_clean.xlsx")

print("="*50)
print("  EMG MUSCLE FATIGUE - ML PIPELINE")
print("="*50)
print(f"\n[1] Dataset loaded: {df.shape[0]} rows")
print(df['Level'].value_counts().to_string())

X = df[['RMS','MAV','ZCR']].values
y = df['Level'].values

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)
print(f"\n[2] Train: {X_train.shape[0]} | Test: {X_test.shape[0]}")

model = RandomForestClassifier(n_estimators=100,max_depth=10,random_state=42,class_weight='balanced')
model.fit(X_train,y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test,y_pred)*100
print(f"\n{'='*50}")
print(f"  ACCURACY: {acc:.2f}%")
print(f"{'='*50}")
print(classification_report(y_test,y_pred,target_names=["Normal","Warning","Fatigue"]))

cv = cross_val_score(model,X,y,cv=5)
print(f"Cross-Val: {cv.mean()*100:.2f}% +/- {cv.std()*100:.2f}%")

cm = confusion_matrix(y_test,y_pred)
fig,ax = plt.subplots(figsize=(7,5))
ConfusionMatrixDisplay(cm,display_labels=["Normal","Warning","Fatigue"]).plot(ax=ax,cmap='Blues')
ax.set_title(f"EMG Fatigue - Confusion Matrix | Accuracy: {acc:.2f}%")
plt.tight_layout()
plt.savefig("confusion_matrix.png",dpi=150)
plt.close()
print("Saved: confusion_matrix.png")

imp = model.feature_importances_
fig,ax = plt.subplots(figsize=(7,4))
ax.barh(['RMS','MAV','ZCR'],imp,color=['#5DCAA5','#1D9E75','#0F6E56'])
ax.set_title("Feature Importance - EMG Fatigue Detection")
plt.tight_layout()
plt.savefig("feature_importance.png",dpi=150)
plt.close()
print("Saved: feature_importance.png")

with open("emg_model.pkl","wb") as f:
    pickle.dump(model,f)
print("Saved: emg_model.pkl")
print("\nALL DONE!")