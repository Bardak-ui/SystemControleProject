import os
path = "media/user_file"


def create_file(code, title_project, user, title_file):
    user = str(user)
    user_dir = os.path.join(path, user)
    project_dir = os.path.join(path,user,title_project)

    os.makedirs(user_dir, exist_ok=True)
    with open(f"{path}/{user}/{title_file}", 'w') as create_file:
        create_file.write(code)
        create_file.close()
    
def edit_file(path, user, title_file):
    pass
        
def delete_file(path, user, title_file, title_project):
    user = str(user)
    os.remove(f"{path}/{user}/{title_project}/{title_file}")