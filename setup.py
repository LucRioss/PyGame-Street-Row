import cx_Freeze

executables = [cx_Freeze.Executable('Street Row.py')]

cx_Freeze.setup(
    name = "Jogo realizado como trabalho para a disciplina de Computação Gráfica",
    options = {'build_exe': {'packages': ['pygame'],
                             'include_files': ['fonte', 'imagens', 'jogador', 'sons']}},

    executables = executables
)
