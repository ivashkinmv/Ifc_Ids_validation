from flask import Flask, request, render_template_string, jsonify, send_file, render_template
import time
import ifcopenshell
import ids
import reporter
import os




app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(open('templates/index.html', 'r', encoding='utf-8').read())

@app.route('/validate', methods=['POST'])
def validate_files():
    file_ifc = request.files['file_ifc']
    file_ids = request.files['file_ids']
    if file_ifc and file_ids:
        # Директория на сервере сюда сохраняются загруженные файлы с web формы
        app.config['UPLOAD_FOLDER'] = r'upload_files'
        file_ifc.save(os.path.join(app.config['UPLOAD_FOLDER'], file_ifc.filename))
        file_ids.save(os.path.join(app.config['UPLOAD_FOLDER'], file_ids.filename))
        start = time.time()

        # Чтение файла IDS через модуль ids.py
        specs = ids.open(os.path.join(app.config['UPLOAD_FOLDER'], file_ids.filename))

        # Чтение файла IFC через IfcOpenShell
        ifc = ifcopenshell.open(os.path.join(app.config['UPLOAD_FOLDER'], file_ifc.filename))
        loading_time = str(time.time() - start)
        print(loading_time)
        start = time.time()

        # Валидация
        specs.validate(ifc)
        validation_time = str(time.time() - start)
        print(validation_time)

        # Формирование отчета в HTML в templates/valid.html.
        # Страница /valid запускается скриптом js после выполнения.
        engine = reporter.Html(specs)
        engine.report()
        engine.to_file("templates/valid.html")

        engine = reporter.Json(specs)
        engine.report()
        engine.to_file("templates/valid.json")

        engine = reporter.Txt(specs)
        engine.report()
        engine.to_file("templates/valid.txt")

        engine = reporter.Bcf(specs)
        engine.report()
        engine.to_file("templates/valid.bcf")

        #Удаление загруженных файлов
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file_ifc.filename))
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file_ids.filename))
        # os.remove('templates/valid.html')

        #Возвращение затраченного времени
        return jsonify(loading_time=loading_time, validation_time=validation_time)

    else:
        return 'Необходимо загрузить оба файла'


#Страница с результатами валидации
@app.route('/valid')
def valid():
    return render_template('valid.html')



if __name__ == '__main__':
    app.run(debug=True)