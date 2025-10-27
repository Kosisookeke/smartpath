/**
 * Courses Page Component
 */
import React, { useState, useEffect } from 'react';
import { courseAPI } from '../services/api';
import CourseCard from '../components/CourseCard';
import './Courses.css';

const Courses = () => {
    const [courses, setCourses] = useState([]);
    const [filteredCourses, setFilteredCourses] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState('All');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadCourses();
    }, []);

    const loadCourses = async () => {
        try {
            const data = await courseAPI.getAll();
            setCourses(data.courses || []);
            setFilteredCourses(data.courses || []);
        } catch (error) {
            console.error('Error loading courses:', error);
        } finally {
            setLoading(false);
        }
    };

    const categories = ['All', ...new Set(courses.map(c => c.category))];

    const filterByCategory = (category) => {
        setSelectedCategory(category);
        if (category === 'All') {
            setFilteredCourses(courses);
        } else {
            setFilteredCourses(courses.filter(c => c.category === category));
        }
    };

    if (loading) {
        return <div className="loading">Loading courses...</div>;
    }

    return (
        <div className="courses-page">
            <div className="page-header">
                <h1>Explore Our Courses</h1>
                <p>Browse through our collection of high-quality learning materials</p>
            </div>

            <div className="filter-section">
                <label>Filter by Category:</label>
                <div className="category-filters">
                    {categories.map(category => (
                        <button
                            key={category}
                            className={`filter-btn ${selectedCategory === category ? 'active' : ''}`}
                            onClick={() => filterByCategory(category)}
                        >
                            {category}
                        </button>
                    ))}
                </div>
            </div>

            <div className="courses-grid">
                {filteredCourses.map(course => (
                    <CourseCard key={course.id} course={course} />
                ))}
            </div>

            {filteredCourses.length === 0 && (
                <div className="empty-state">
                    <p>No courses found in this category.</p>
                </div>
            )}
        </div>
    );
};

export default Courses;

