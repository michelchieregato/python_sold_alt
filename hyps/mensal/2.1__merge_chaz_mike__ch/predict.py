import pandas as pd
from xgboost import XGBRegressor
from sklearn.externals import joblib
from sklearn.preprocessing import LabelEncoder

TAMANHO_VAL = {
    '00': 0,
    '02': 1,
    '04': 2,
    '06': 3,
    '08': 4,
    '10': 5,
    '12': 6,
    '14': 7,
    'PP': 8,
    'P': 9,
    'M': 10,
    'G': 11,
    'GG': 12
}

PARAMS = {
    'max_depth': 7,
    'subsample': .85,
    'colsample_bylevel': 1,
    'n_estimators': 600,
    'learning_rate': .025,
    'random_state': 40,  # 1
    'silent': 0,
    'reg_alpha': .1,
    'eval_metric': 'rmse',
}


def pre_proc(src, test=True):
    df = pd.read_csv(src)
    le_desc = LabelEncoder()
    df['DESCRICAO'] = le_desc.fit_transform(df.DESCRICAO)
    df.TAMANHO = df.TAMANHO.apply(lambda x: TAMANHO_VAL[x])
    le_nome = LabelEncoder()
    df['NOME'] = le_nome.fit_transform(df.NOME)

    desc_mes = df.groupby(['DESCRICAO', 'MES']).QUANTIDADE.sum().reset_index(name='DESCRICAO_MES')
    df = df.merge(desc_mes, on=['DESCRICAO', 'MES'], how='left')
    desc_place = df.groupby(['DESCRICAO', 'NOME']).QUANTIDADE.sum().reset_index(name='DESCRICAO_NOME')
    df = df.merge(desc_place, on=['DESCRICAO', 'NOME'], how='left')
    if not test:
        x = df.drop('QUANTIDADE', axis=1)
        y = df['QUANTIDADE']
        return x, y
    else:
        try:
            df = df.drop('QUANTIDADE', axis=1)
        except:
            pass
        return df


def retrain(src):
    x, y = pre_proc(src, test=False)
    xgb = XGBRegressor(**PARAMS)
    xgb.fit(x, y)
    joblib.dump(xgb, 'model.dat')
    return xgb


def predict(model, test):
    return model.predict(test)


def execute(do_retrain=False, src_train='../../../data/interim/Vendas_treino.csv', src_test='../../../data/interim/Vendas_test.csv', model='model.dat'):
    if do_retrain:
        new_model = retrain(src_train)
    else:
        new_model = joblib.load(model)
    test_data = pre_proc(src_test)
    sells = predict(new_model, test_data)
    return sells

if __name__ == '__main__':
    print(execute(do_retrain=True))
