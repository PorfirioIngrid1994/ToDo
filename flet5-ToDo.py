import flet
from flet import (
    Checkbox,
    Column,
    FloatingActionButton,
    IconButton,
    OutlinedButton,
    Page,
    Row,
    Tab,
    Tabs,
    Text,
    TextField,
    UserControl,
    colors,
    icons,
)  # Importação dos componentes utilizados na aplicação


# Classe de tarefas (Classe Principal):
class Task(UserControl):
    def __init__(self, task_name, task_status_change, task_delete):
        super().__init__()
        self.completed = False
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete
    
    def build(self):
        self.display_task = Checkbox(
            value=False, label=self.task_name, on_change=self.status_changed
        )

        self.edit_name = TextField(expand=1)  # Entrada de texto da edição da tarefa

        self.display_view = Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.display_task, 
                Row(
                    spacing=0, 
                    controls=[
                        IconButton(
                            icon=icons.CREATE_OUTLINED,
                            tooltip="Editar tarefa",  # Mostra uma informação quando passa o mouse por cima do botão
                            on_click=self.edit_clicked,
                            icon_color=colors.GREEN,
                        ),
                        IconButton(
                            icon=icons.DELETE_OUTLINED,
                            tooltip="Deletar tarefa",  # Mostra uma informação quando passa o mouse por cima do botão
                            on_click=self.delete_clicked,
                            icon_color=colors.RED,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = Row(
            visible=False, 
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                IconButton(
                    icon=icons.DONE_OUTLINE,
                    icon_color=colors.GREEN,
                    tooltip="Atualizar tarefa", 
                    on_click=self.save_clicked, 
                )
            ]
        )

        return Column(controls=[self.display_view, self.edit_view])
    
    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_name.visible = True
        self.update()

    def delete_clicked(self, e):
        self.task_delete(self)

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_status_change(self)

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()
        
# Classe da aplicação toda: 

class ToDoApp(UserControl):
    def __init__(self):
        super().__init__()
        self.items_left = Text(value="0 Tarefas adicionadas")  # Inicializa o atributo items_left

    def build(self):
        self.new_task = TextField(
            hint_text="Escreva a sua tarefa",
            expand=True,
            on_submit=self.add_clicked,
        )
        self.tasks = Column()

        # Criando as tabs
        self.filter = Tabs(
            selected_index=0, 
            on_change=self.tabs_changed,  # Onde for mexido
            tabs=[Tab(text="Todas as tarefas"), Tab(text="Tarefas Ativas"), Tab(text="Tarefas Concluídas")],
        )

        return Column(
            width=600, 
            controls=[
                Row([Text(value="Tarefas", style="headlineMedium")], alignment="center"),
                Row(
                    controls=[
                        self.new_task, 
                        FloatingActionButton(icon=icons.ADD, on_click=self.add_clicked)
                    ],
                ),
                self.filter,
                self.tasks,
                Row(
                    alignment="spaceBetween", 
                    vertical_alignment="center",
                    controls=[
                        self.items_left, 
                        OutlinedButton(
                            text="Limpar Tarefas",
                            on_click=self.clear_clicked,
                        ),
                    ],
                ),
            ],
        )

    def add_clicked(self, e):
        if self.new_task.value:
            task = Task(self.new_task.value, self.task_status_change, self.task_delete)
            self.tasks.controls.append(task)
            self.new_task.value = ""
            self.new_task.focus()
            self.update()

    def task_status_change(self, task):
        self.update()
        
    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    def tabs_changed(self, e):
        self.update()

    def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                self.task_delete(task)

    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0 

        for task in self.tasks.controls:
            task.visible = (
                status == "Todas as tarefas"
                or (status == "Tarefas Ativas" and not task.completed)
                or (status == "Tarefas Concluídas" and task.completed)             
            )

            if not task.completed:
                count += 1
        self.items_left.value = f"{count} Tarefas adicionadas"
        super().update()

# Função Principal:
def main(page: Page):
    page.title = "Tarefas"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"

    # Instancia a classe principal
    app = ToDoApp()

    # Chama a função build() da classe ToDoApp
    app.build()

    # Adiciona a aplicação na página
    page.add(app)

    page.update()

flet.app(target=main)
