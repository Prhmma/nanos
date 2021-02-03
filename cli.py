import requests
from similarity import similarity
from validator_collection import validators
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def user_input():
    try:
        url = validators.url(input("Enter the URL: "))
    except Exception as ex:
        print(ex)
        return
    products_services = input("Ener Products/services (seperate by ','): ")
    _similarity = float(input("Enter similarity ratio between 0 and 1: "))
    return url, products_services, _similarity


def similarity_process():
    url, products_services, similarity_ratio = user_input()
    result = {}
    output_string = ""
    word_cloud = {}
    web_page = requests.get(url, verify = False)
    if web_page.status_code == 200:
        simimilarity_object = similarity(products_services, web_page.text)
        simimilarity_object.pre_processing()
        result = simimilarity_object.similarity_detection(json_output=False)
        for item in result:
            if item[1] > similarity_ratio:
                output_string += item[0] + ", "
                word_cloud[item[0]] = item[1]
    return output_string,word_cloud


def main():
    output_string,word_cloud = similarity_process()
    print(output_string)
    wc = WordCloud()
    wc.generate_from_frequencies(word_cloud)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    main()