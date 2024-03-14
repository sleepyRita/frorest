from django.shortcuts import render
from django.http import JsonResponse
import json
import pandas as pd
from sklearn.ensemble import RandomForestRegressor


# Create your views here.


def upload(request):

    if request.method == "GET":
        return JsonResponse({"status": "failed"})

    params = json.loads(request.body)
    data = params["data"]
    keys = list(data[0].keys())

    return JsonResponse(
        {
            "status": "ok",
            "data": keys,
        }
    )


def submit(request):

    if request.method == "GET":
        return JsonResponse({"status": "failed"})

    params = json.loads(request.body)
    data = params["data"]

    ind_list = params["indList"]
    dep = params["dependent"]

    df = pd.DataFrame(data)
    X = df[ind_list]
    y = df[dep]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    feature_importance = model.feature_importances_
    importance_dict = dict(zip(ind_list, feature_importance))

    for key, value in importance_dict.items():
        importance_dict[key] = round(value, 3)

    return JsonResponse(
        {
            "status": "ok",
            "data": importance_dict,
        }
    )
