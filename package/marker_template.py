
def apply_template(dict_results):
    info_box_template = """
    <dl>
    <dt>Cajero:</dt><dd>{name}</dd>
    <dt>Comisión:</dt><dd>{COMISION_1}€</dd>
    <dt>Dirección:</dt><dd>{vicinity}</dd>
    </dl>
    """
    atm_info = [info_box_template.format(**atm) for atm in dict_results]
    return atm_info
