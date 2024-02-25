import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import firebase_admin
import io
from google.cloud import storage
from firebase_admin import credentials as admin_credentials  # Firebase용 credentials로 명칭 변경
from firebase_admin import firestore
from google.cloud import storage
from google.oauth2 import service_account  # Google Cloud Storage용
import os
import tempfile

# Firebase Admin SDK를 위한 서비스 계정 키 파일 경로
firebase_key_path = "serviceAccountKey.json"

# Firebase Admin SDK 초기화
firebase_cred = admin_credentials.Certificate(firebase_key_path)
firebase_admin.initialize_app(firebase_cred)

# Google Cloud Storage 클라이언트 생성을 위한 서비스 계정 키 경로
gcs_credentials = service_account.Credentials.from_service_account_file(firebase_key_path)

# 인증 정보를 사용하여 Google Cloud Storage 클라이언트 생성
storage_client = storage.Client(credentials=gcs_credentials, project=gcs_credentials.project_id)

# Firebase Storage에서 사용하는 버킷 이름
bucket_name = 'hearos-414916.appspot.com'
bucket = storage_client.bucket(bucket_name)

# 파일 경로 설정
file_path = "voice/voice.mp3"
blob = bucket.blob(file_path)
blob.download_to_file(io.BytesIO())


# 수정된 부분: 파일 바이트 스트림을 직접 librosa.load에 전달
file_stream = io.BytesIO()
blob.download_to_file(file_stream)
file_stream.seek(0)  # 스트림의 시작으로 포인터를 이동
y, sr = librosa.load(file_stream, sr=None)

mfccs = librosa.feature.mfcc(y=y, sr=sr)

#print(y)
#print(len(y))
#print('Sampling rate (Hz): %d' %sr) #헤르츠 
#print('Audio length (seconds): %.2f' % (len(y) / sr)) #음악의 길이(초) = 음파의 길이/Sampling rate


#피치(F0) 추출
# 높다/낮다 
f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
valid_f0 = f0[voiced_flag]
average_pitch = np.mean(valid_f0)

#print(f'Average Pitch (Hz): {average_pitch:.2f}')

# 피치 높낮이 판단
#pitch_threshold = 150
#if average_pitch > pitch_threshold:
   # print("The pitch is high.")
#else:
    #print("The pitch is low.")

# 1. MFCCs 추출
mfccs = librosa.feature.mfcc(y=y, sr=sr)
avg_mfccs = np.mean(mfccs, axis=1)

# MFCCs 높낮이 판단 (어떤 스펙트럼에 분포가 큰지 파악, 높다/낮다)
mfccs_threshold = 0
mfccs_result = 0 if avg_mfccs[0] > mfccs_threshold else 1

if avg_mfccs[0] > mfccs_threshold:
    print("The MFCCs indicate a higher spectral energy concentration at lower frequencies.")
else:
    print("The MFCCs indicate a lower spectral energy concentration at lower frequencies.")

# 2. 스펙트럼 센트로이드 계산(밝다/어둡다)
spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
avg_spectral_centroid = np.mean(spectral_centroids)

# 스펙트럼 센트로이드 높낮이 판단
spectral_centroid_threshold = 3000
spectral_centroid_result = 0 if avg_spectral_centroid > spectral_centroid_threshold else 1

if avg_spectral_centroid > spectral_centroid_threshold:
    print("The sound is brighter.")
else:
    print("The sound is darker.")



# 3.제로 크로싱 레이트 계산(모노톤/리드미컬)
zcr = np.sum(librosa.feature.zero_crossing_rate(y)[0])

# ZCR에 따른 모노톤/리드미컬함 판단
zcr_threshold = 0.1
zcr_result = 0 if zcr > zcr_threshold else 1
if zcr > zcr_threshold:
    print("The signal is rhythmic.")
else:
    print("The signal is monotone.")


# 4. 에너지 추출(강/약)
energy = np.mean(np.square(y))

# 에너지 높낮이 판단 기준 
energy_threshold = 0.01
energy_result = 0 if energy > energy_threshold else 1
if energy > energy_threshold:
    print("The energy is high.")
else:
    print("The energy is low.")




# 1. 분석 결과를 문자열로 조합
analysis_results = f"""
{mfccs_result}
{spectral_centroid_result}
{zcr_result}
{energy_result}
"""

# 분석 결과를 리스트로 조합
analysis_results_list = [mfccs_result, spectral_centroid_result, zcr_result, energy_result]

# 리스트를 문자열로 변환하여 저장
analysis_results_str = str(analysis_results_list)

print(analysis_results_list)

# 2. 임시 파일에 분석 결과를 저장
# tempfile 모듈을 사용하여 임시 파일 생성
with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.txt') as temp_file:
    temp_file.write(analysis_results)
    temp_file_path = temp_file.name

# 3. Firebase Storage에 파일 업로드
# 'hearo-2024' 버킷에 'analysis_results.txt'라는 이름으로 저장
upload_blob = bucket.blob('string/analysis_results.txt')
upload_blob.upload_from_filename(temp_file_path)

# 임시 파일 삭제
os.remove(temp_file_path)
