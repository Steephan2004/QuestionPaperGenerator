import React, { useState, useEffect } from 'react';
import './SubjectForm.css';

const SubjectForm = () => {
  const [selectedCode, setSelectedCode] = useState('');
  const [selectedName, setSelectedName] = useState('');
  const [selectedYear, setSelectedYear] = useState('');
  const [selectedSemester, setSelectedSemester] = useState('');
  const [selectedDept, setSelectedDept] = useState('');
  const [selectedStaffName, setSelectedStaffName] = useState('');
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchSubjects();
  }, []);

  const fetchSubjects = async () => {
    try {
      const response = await fetch("http://192.168.0.4:8000/get_subjects");
      const jsonData = await response.json();
      setData(jsonData);
      console.log(jsonData);
    } catch (error) {
      console.log(error);
    }
  };

  // Filtered data for each dropdown
  const filteredData = data.filter((subject) => {
    return (
      (!selectedYear || subject.year === selectedYear) &&
      (!selectedSemester || subject.semester === selectedSemester) &&
      (!selectedDept || subject.department === selectedDept) &&
      (!selectedStaffName || subject.staffname === selectedStaffName)
    );
  });

  const handleCodeChange = (e) => {
    setSelectedCode(e.target.value);
    const subject = data.find((sub) => sub.subjectCode === e.target.value);
    setSelectedName(subject ? subject.subjectName : '');
  };

  const handleNameChange = (e) => {
    setSelectedName(e.target.value);
    const subject = data.find((sub) => sub.subjectName === e.target.value);
    setSelectedCode(subject ? subject.subjectCode : '');
  };

  const handleYearChange = (e) => setSelectedYear(e.target.value);
  const handleSemesterChange = (e) => setSelectedSemester(e.target.value);
  const handleDeptChange = (e) => setSelectedDept(e.target.value);
  const handleStaffNameChange = (e) => setSelectedStaffName(e.target.value);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://192.168.0.4:8000/pdf/?subject_code=${selectedCode}&year=${selectedYear}&dept=${selectedDept}&sem=${selectedSemester}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/pdf',
        },
      });

      if (!response.ok) {
        throw new Error('Network response was not ok: ' + response.statusText);
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'Question Paper.pdf');
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

    } catch (error) {
      alert('Error generating PDF: ' + error.message);
      console.error('Error generating PDF:', error);
    }
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit} className="subject-form">
        <h2 className="form-title">Subject Selection</h2>

        <div className="form-group">
          <label htmlFor="academicYear">Academic Year</label>
          <select
            id="academicYear"
            value={selectedYear}
            onChange={handleYearChange}
            className="form-control"
          >
            <option value="">Select Academic Year</option>
            <option value="2024-2025">2024-2025</option>
            <option value="2025-2026">2025-2026</option>
            <option value="2026-2027">2026-2027</option>
            <option value="2027-2028">2027-2028</option>
            <option value="2028-2029">2028-2029</option>
          </select>
        </div>  

        <div className="form-group">
          <label htmlFor="semester">Semester</label>
          <select
            id="semester"
            value={selectedSemester}
            onChange={handleSemesterChange}
            className="form-control"
          >
            <option value="">Select Semester</option>
            <option value="Even">Even</option>
            <option value="Odd">Odd</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="department">Department</label>
          <select
            id="department"
            value={selectedDept}
            onChange={handleDeptChange}
            className="form-control"
          >
            <option value="">Select Department</option>
            <option value="CSE">CSE</option>
            <option value="ECE">ECE</option>
            <option value="EEE">EEE</option>
            <option value="CIVIL">CIVIL</option>
            <option value="MECH">MECH</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="staffName">Staff Name</label>
          <select
            id="staffName"
            value={selectedStaffName}
            onChange={handleStaffNameChange}
            className="form-control"
          >
            <option value="">Select Staff Name</option>
            {[...new Set(filteredData.map((subject) => subject.staffname))].map((name, index) => (
              <option key={index} value={name}>
                {name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="subjectCode">Subject Code</label>
          <select
            id="subjectCode"
            value={selectedCode}
            onChange={handleCodeChange}
            className="form-control"
          >
            <option value="">Select Subject Code</option>
            {filteredData.map((subject, index) => (
              <option key={index} value={subject.subjectCode}>
                {subject.subjectCode}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="subjectName">Subject Name</label>
          <select
            id="subjectName"
            value={selectedName}
            onChange={handleNameChange}
            className="form-control"
          >
            <option value="">Select Subject Name</option>
            {filteredData.map((subject, index) => (
              <option key={index} value={subject.subjectName}>
                {subject.subjectName}
              </option>
            ))}
          </select>
        </div>

        <button type="submit" className="submit-button">Generate Question Paper</button>
      </form>
    </div>
  );
};

export default SubjectForm;
