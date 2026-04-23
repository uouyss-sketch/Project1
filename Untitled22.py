{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "toc_visible": true,
      "authorship_tag": "ABX9TyOYcyHpLKitXXwDOqTO5pTv",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/uouyss-sketch/Project1/blob/main/Untitled22.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "BjUEbEiAG85R",
        "outputId": "4ce904d8-7de5-42d6-9499-cff626012330"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "저장 완료: {'수집시간': '2026-04-23 07:00:01', '미국(USD)': '1,481.50', '코스피(KOSPI)': '6,475.81'}\n"
          ]
        }
      ],
      "source": [
        "import requests\n",
        "from bs4 import BeautifulSoup\n",
        "import pandas as pd\n",
        "from datetime import datetime\n",
        "\n",
        "# 1. 정보 수집 함수 정의\n",
        "def get_finance_data():\n",
        "    url = \"https://finance.naver.com/marketindex/\"\n",
        "    res = requests.get(url)\n",
        "    soup = BeautifulSoup(res.text, 'html.parser')\n",
        "\n",
        "    # 데이터 추출\n",
        "    usd_rate = soup.select_one('div.head_info > span.value').text # 환율\n",
        "    kospi_index = soup.select_one('span.num_quot > #now_value').text if soup.select_one('#now_value') else \"데이터없음\"\n",
        "\n",
        "    # 코스피를 다른 경로에서 가져오기 (만약 위 경로가 안될 경우)\n",
        "    kospi_url = \"https://finance.naver.com/sise/\"\n",
        "    res_k = requests.get(kospi_url)\n",
        "    soup_k = BeautifulSoup(res_k.text, 'html.parser')\n",
        "    kospi_index = soup_k.select_one('#KOSPI_now').text\n",
        "\n",
        "    # 현재 시간 기록\n",
        "    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')\n",
        "\n",
        "    return {\n",
        "        \"수집시간\": now,\n",
        "        \"미국(USD)\": usd_rate,\n",
        "        \"코스피(KOSPI)\": kospi_index\n",
        "    }\n",
        "\n",
        "# 2. 실행 및 저장\n",
        "data = get_finance_data()\n",
        "df = pd.DataFrame([data])\n",
        "\n",
        "# 기존에 파일이 있으면 이어서 붙이고, 없으면 새로 생성 (A 버튼 클릭 효과)\n",
        "file_name = 'finance_data_log.xlsx'\n",
        "try:\n",
        "    existing_df = pd.read_excel(file_name)\n",
        "    df = pd.concat([existing_df, df], ignore_index=True)\n",
        "except FileNotFoundError:\n",
        "    pass\n",
        "\n",
        "df.to_excel(file_name, index=False)\n",
        "print(f\"저장 완료: {data}\")"
      ]
    }
  ]
}