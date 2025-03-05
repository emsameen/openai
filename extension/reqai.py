import vscode
from vscode import InfoMessage

ext = vscode.Extension(name="ReqAI")


@ext.command()
async def swf_check_requiremenets(ctx: vscode.Context):
    messsage = InfoMessage(f"Check Requirements Quality {ext.display_name}")
    await ctx.window.show(messsage)

@ext.command()
async def swf_generate_tests(ctx: vscode.Context):
    messsage = InfoMessage(f"Generate Tests Cases {ext.display_name}")
    await ctx.window.show(messsage)

ext.run()