Reiks situ (pasigooglinkit kaip instaliuot jei neturit)

 - Python 3.12+ (prob ir senesnes veik)
 - uv (python manager)
 ---
<br>
<br>
<br>
<br>

init project:
```
uv sync
uv run python manage.py migrate
uv run python manage.py seed_demo
uv run python manage.py tailwind install
uv run python manage.py tailwind build
```

to run program:
```
uv run python manage.py runserver
```

<br>
<br>
<br>
<br>

---
before commiting run
on windows:
``` powershell
test.ps1
```

on linux:
``` bash
test.sh
```