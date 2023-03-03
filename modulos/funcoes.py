import discord

def pegar_posicao_str(string = str, subs = str, occorencia = int):
    """Procura a posição de uma substring em uma string.

    Args:
        string (str): string principal
        subs (str): substring dentro da string
        ocorrencia (int): numero da ocorrência da substring

    Returns:
        int: Posição da substring na ocorrência especificada 
    """

    start = string.find(subs)
    
    while start >= 0 and occorencia > 1:
        start = string.find(subs, start+1)
        occorencia -= 1

    return start


async def mandar_embed(
    titulo: str = None,
    desc: str = None, 
    autor: str = None, 
    autoricon: str = None,
    titfield: str = None,
    descfield: str = None,
    inlifield=True,
    esconder=False,
    *,
    contexto=None,
    ):

    """Manda uma embed no contexto da mensagem

    Args:
        contexto (_type_, optional): ctx do comando usado. Defaults to None.
        titulo (str, optional): titulo da embed. Defaults to None.
        desc (str, optional): descrição da embed. Defaults to None.
        autor (str, optional): autor da embed. Defaults to None.
        autoricon (str, optional): Icon do autor da embed. Defaults to None.
        titfield (str, optional): Titulo da field. Defaults to None.
        descfield (str, optional): Descrição da field. Defaults to None.
        inlifield (bool, optional): Se a field criada será inline ou não. Defaults to True.
        esconder (bool, optional): valor ephemeral da embed, mostrar somente ao usuário. Defaults to False.

    Returns:
        comando ctx.send para mandar a embed definida na função
    """

    embed = discord.Embed(
        title = titulo, 
        description = desc, 
        colour = 0xdfca7f
    )

    if autor != None:
        embed.set_author(
            name= autor,
            icon_url= autoricon
    )

    if titfield != None: 
        embed.add_field(
            name = titfield, 
            value = descfield, 
            inline = inlifield
        )

    return await contexto.send(
        embed = embed, 
        ephemeral = esconder
    )
