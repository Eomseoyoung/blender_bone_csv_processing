def calculate_unit_length(data):
    """
    몸통 길이를 기반으로 단위 길이를 계산합니다.
    단위 길이 = (어깨 중앙-엉덩이 중앙 거리) + (엉덩이 중앙-무릎 중앙 거리)
    필요한 관절 좌표 중 하나라도 NaN이면, 계산 결과도 NaN이 됩니다.

    Args:
        data (pd.DataFrame or pd.Series): 키포인트 좌표 데이터.
            - DataFrame: 여러 프레임의 데이터.
            - Series: 단일 프레임의 데이터.

    Returns:
        pd.Series or float: 계산된 단위 길이. DataFrame 입력 시 Series, Series 입력 시 float 반환.
    """
    # COCO 기준: left_shoulder(5), right_shoulder(6), left_hip(11), right_hip(12), left_knee(13), right_knee(14)
    # 입력 데이터가 Series일 경우, .get()을 사용하여 안전하게 값에 접근
    mid_shoulder = (np.array([data.get('5_x'), data.get('5_y')]) + np.array([data.get('6_x'), data.get('6_y')])) / 2
    mid_hip = (np.array([data.get('11_x'), data.get('11_y')]) + np.array([data.get('12_x'), data.get('12_y')])) / 2
    mid_knee = (np.array([data.get('13_x'), data.get('13_y')]) + np.array([data.get('14_x'), data.get('14_y')])) / 2

    # 중앙점 간의 유클리드 거리 계산
    dist_shoulder_hip = np.linalg.norm(mid_shoulder - mid_hip, axis=0)
    dist_hip_knee = np.linalg.norm(mid_hip - mid_knee, axis=0)
    
    # 단위 길이 계산 (두 거리의 합)
    unit_length = dist_shoulder_hip + dist_hip_knee
    return pd.Series(unit_length, index=data.index) if isinstance(data, pd.DataFrame) else unit_length




    def unreal_process_csv_batch(self, filepath: str) -> pd.DataFrame:
        """CSV 파일을 읽어 일괄적으로 정규화합니다."""
        df = pd.read_csv(filepath, index_col=0)
        df = self._normalize_unreal_column_names(df)

        # --- Step 1: 데이터 무결성 적용 ---
        df.replace(0.0, np.nan, inplace=True)

        # --- Step 2: 단위 길이 계산 ---
        df['unit_length'] = calculate_unit_length(df)
        df['unit_length'].fillna(method='ffill', inplace=True)
        df['unit_length'].fillna(method='bfill', inplace=True)
        df['unit_length'] = df['unit_length'].clip(lower=1e-6)

        # --- Step 3: 단위 길이 기반 좌표 정규화 ---
        coord_cols = [col for col in df.columns if '_x' in col or '_y' in col]
        
        # COCO 기준: left_hip(11), right_hip(12)
        df['mid_hip_x'] = (df['11_x'] + df['12_x']) / 2
        df['mid_hip_y'] = (df['11_y'] + df['12_y']) / 2
        df['mid_hip_x'].fillna(method='ffill', inplace=True)
        df['mid_hip_y'].fillna(method='ffill', inplace=True)
        df['mid_hip_x'].fillna(method='bfill', inplace=True)
        df['mid_hip_y'].fillna(method='bfill', inplace=True)

        for col in coord_cols:
            axis = col.split('_')[-1]
            df[col] = (df[col] - df[f'mid_hip_{axis}']) / df['unit_length']

        # --- Step 4: 상하 반전 (y축 반전) ---
        y_cols = [col for col in df.columns if '_y' in col]
        df[y_cols] *= -1

        df.drop(columns=['unit_length', 'mid_hip_x', 'mid_hip_y'], inplace=True)
        return df