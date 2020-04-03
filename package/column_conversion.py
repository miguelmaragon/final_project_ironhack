def rename_f(join):
    if 'bbva' in join:
        return 'bbva'
    elif 'santander' in join:
        return 'santander'
    elif 'kutxabank' in join:
        return 'kutxabank'
    elif 'bankia' in join:
        return 'bankia'
    elif 'unicaja' in join:
        return 'unicaja'
    elif 'ibercaja' in join:
        return 'ibercaja'
    elif 'caixabank' in join:
        return 'caixabank'
    elif 'popular' in join:
        return 'popular'
    elif 'ing direct' in join:
        return 'ing_direct'
    elif 'sabadell' in join:
        return 'sabadell'
    elif 'openbank' in join:
        return 'openbank'
    elif 'abanka' in join:
        return 'abanka'
    elif 'liberbank' in join:
        return 'liberbank'
    elif 'deutsche' in join:
        return 'deutsche'
    elif 'bankinter' in join:
        return 'bankinter'
    else:
        return 'Otros'


def title_column(df, column):
    df = df.copy()
    df[column] = df[column].str.title()
    return df[column]