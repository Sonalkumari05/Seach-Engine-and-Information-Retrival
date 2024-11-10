import os
import math

### author Sonal Kumari
### date 25 April, 2024
### change the folder_path in the main function with the path you have to read


def read_files_in_folder(folder_path):
    """ 
    reads the argument folder_path and returns the list as filenames
    tokens_list which is a list of all the tokens from the document
    dic_docId_doc is dictionary where keys are id like 1, 2, 3 etc and values are list of all the tokens of that document

    folder_path: path of the folder to read

    """
    filenames = []
    tokens_list = []
    dic_docId_doc = {}
    n = 1
    for filename in os.listdir(folder_path):
        with open(os.path.join(folder_path, filename), 'r') as file:
            content = file.read()
            tokens = content.split()  
            tokens_list.append(tokens)
            dic_docId_doc[n] = tokens
            n += 1
            filenames.append(filename)
    return filenames, tokens_list, dic_docId_doc

def tokenize_document(document):
    """
    return a list of tokens

    documnet: the document whose token is to convert
    """
    tokens = []
    current_token = ""
    for char in document:
        if char.isalnum() or char == '_':
            current_token += char
        elif current_token :
            tokens.append(current_token)
            current_token = ""
    if current_token:
        tokens.append(current_token)
    return tokens


def dict_tokens(tokens_list):
    """
    returns a dict_tokenId which is a dictionary in which keys are tokens and values are id like 1, 2, 3 etc

    tokens_list: list of tokens
    """
    dict_tokenId = {}
    num = 1
    for token in tokens_list:
        if token not in dict_tokenId:
            dict_tokenId[token] = num
            num += 1
    return dict_tokenId


def dict_weights(tokens_list):
    """
    return a tokens_weights which is a dictionary of tokens as keys and its frequency in tokens_list

    tokens_list: list of all the tokens
    """
    tokens_weights = {}
    for token in tokens_list:
        if token not in tokens_weights:
            tokens_weights[token] = 1
        else:
            tokens_weights[token] = tokens_weights[token] + 1
    return tokens_weights


def compute_tokens_idf(tokens_list):
    """
    returns a dictionary token_idf where keys are tokens and its values are idf 

    tokens_list: list of all the tokens

    """
    tokens_idf = {}
    total_docs = 132
    for tokens in tokens_list:
        unique_tokens = set(tokens)
        for token in unique_tokens:
            if token in tokens_idf:
                tokens_idf[token] += 1
            else:
                tokens_idf[token] = 1
    
    for token, count in tokens_idf.items():
        tokens_idf[token] = math.log(total_docs / count)
    
    return tokens_idf

def tf_idf(tokens_weights, tokens_idf):
    """
    returns a dictionary of tokens as key and tf*idf as values

    token_weights: dictionary of tokens  as keys and their weights as values

    tokens_idf: dictionary if tokens and keys and idf as value
    
    """
    tf_idf = {}
    for token, weight in tokens_weights.items():
        tf_idf[token] = weight * tokens_idf.get(token, 0)
    return tf_idf


def calculate_cosine_similarity(dict_tf_idf1, dict_tf_idf2):
    """
    returns cosine_similarity between two documents

    dict_tf_idf1 : dictionary of token as keys and tf*idf of that token as values of first document

    dict_tf_idf2 : dictionary of token as keys and tf*idf of that token as values of second document

    """
    dot_product = 0
    norm_a = 0
    norm_b = 0
    for token, tf_idf1 in dict_tf_idf1.items():
        tf_idf2 = dict_tf_idf2.get(token, 0)
        dot_product += tf_idf1 * tf_idf2
        norm_a += tf_idf1 ** 2
        norm_b += tf_idf2 ** 2
    
    return dot_product / (math.sqrt(norm_a) * math.sqrt(norm_b))

def main(folder_path):
    filenames, tokens_list, dic_docId_doc = read_files_in_folder(folder_path)
    tokens_idf = compute_tokens_idf(tokens_list)
    result_dict = {}
    
    for i in range(1, 133):
        for j in range(i + 1, 133):
            tokens_weights_id_i = dict_weights(dic_docId_doc[i])
            tokens_weights_id_j = dict_weights(dic_docId_doc[j])

            dict_tf_idf1 = tf_idf(tokens_weights_id_i, tokens_idf)
            dict_tf_idf2 = tf_idf(tokens_weights_id_j, tokens_idf)

            similarity = calculate_cosine_similarity(dict_tf_idf1, dict_tf_idf2)
            result_dict[(i, j)] = similarity
    
    result_dict = dict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True))
    i = 0
    for doc in result_dict:
        if i != 50:
            print('Similarity between', filenames[doc[0]-1], 'and', filenames[doc[1]-1], 'is', result_dict[doc])
            i += 1
        else:
            return

if __name__ == "__main__":
    folder_path = "C:\\Users\\LENOVO\\Downloads\\25-20240411T071922Z-001\\25"
    main( folder_path)
