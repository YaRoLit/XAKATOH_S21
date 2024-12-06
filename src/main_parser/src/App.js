import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const FileUpload = () => {
  const [files, setFiles] = useState([]);
  const [status, setStatus] = useState("");
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleFileChange = (event) => {
    setFiles(event.target.files);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();

    // Добавляем все файлы в formData с ключом 'file'
    for (let i = 0; i < files.length; i++) {
      formData.append("file", files[i]);
    }

    try {
      setStatus("Загружается...");
      setUploadProgress(0);  // Сбрасываем прогресс

      const response = await axios.post("http://localhost:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        responseType: "blob",  // Ожидаем файл в ответе
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                  
        // Уменьшаем прогресс на 50% (или используйте другой коэффициент для замедления)
        const slowedProgress = Math.min(Math.round(percentCompleted * 0.5), 100);

        setUploadProgress(slowedProgress);
        },
      });

      setStatus("Загрузка завершена!");
      setUploadProgress(100);  // Устанавливаем 100% после завершения загрузки

      // Симулируем обработку файлов
      setStatus("Файлы обрабатываются...");
      setTimeout(() => {
        // После обработки (по истечении времени) показываем финальный статус
        setStatus("Обработка завершена!");

        // Создаем ссылку для скачивания Excel-файла
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "Otkaz.xlsx");
        document.body.appendChild(link);
        link.click();
      }, 3000);  // Задержка обработки 3 секунды (можно заменить на реальное время с сервера)

    } catch (error) {
      setStatus("Ошибка загрузки.");
      setUploadProgress(0);  // В случае ошибки сбрасываем прогресс
      console.error("Upload error:", error);
    }
  };

  const handleDatabaseExport = async () => {
    try {
      setStatus("Выгрузка базы данных...");

      const response = await axios.get("http://localhost:5000/export-db", {
        responseType: "blob",  // Ожидаем файл в ответе
      });

      setStatus("Выгрузка завершена!");

      // Создаем ссылку для скачивания выгрузки базы данных
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "output.xlsx");
      document.body.appendChild(link);
      link.click();
    } catch (error) {
      setStatus("Ошибка при выгрузке базы данных.");
      console.error("Database export error:", error);
    }
  };

  return (
    <div className="file-upload-container">
      <img src="/logo.png" alt="Логотип" className="file-upload-logo" />
      <form className="file-upload-form" onSubmit={handleSubmit}>
        <h1 className="file-upload-title">Загрузка файлов</h1>
        <input
          type="file"
          multiple
          className="file-upload-input"
          onChange={handleFileChange}
        />
        <button type="submit" className="file-upload-button">
          Загрузить
        </button>
      </form>
      <div className="file-upload-progress-container">
        <div
          className="file-upload-progress-bar"
          style={{ width: `${uploadProgress}%` }}
        ></div>
      </div>
      <p className="file-upload-status">{status}</p>
      <button
        className="file-upload-db-button"
        onClick={handleDatabaseExport}
      >
        Выгрузить БД
      </button>
    </div>
  );
};

export default FileUpload;
