import math

import pytest

from utils.math.vector import Vector


@pytest.fixture
def vec_a() -> Vector:
    return Vector(3, 4)


@pytest.fixture
def vec_b() -> Vector:
    return Vector(1, -2)


class TestVector:
    def test_zero_returns_origin(self):
        assert Vector.zero() == Vector(0.0, 0.0)

    def test_length(self, vec_a: Vector):
        assert vec_a.length == 5
    
    def test_arg(self, vec_a: Vector):
        assert vec_a.arg == math.atan2(4, 3)

    def test_normalize(self, vec_a: Vector):
        normalized = vec_a.normalize()
        assert normalized == Vector(3 / 5, 4 / 5)

    def test_normalize_zero_vector_is_safe(self):
        assert Vector.zero().normalize() == Vector.zero()

    def test_add_angle(self, vec_a: Vector):
        rotated = vec_a.add_angle(math.pi / 2)
        assert pytest.approx(rotated.x, rel=1e-6) == -0.8
        assert pytest.approx(rotated.y, rel=1e-6) == 0.6

    def test_to_tuple(self, vec_a: Vector):
        assert vec_a.to_tuple() == (3, 4)
    
    # ===== ADDITION =====
    def test_componentwise_addition(self, vec_a: Vector, vec_b: Vector):
        assert vec_a + vec_b == Vector(4, 2)

    def test_scalar_addition(self, vec_a: Vector, vec_b: Vector):
        assert vec_a + 2 == Vector(5, 6)
        assert 2 + vec_a == Vector(5, 6)
    
    def test_scalar_addition_inplace(self, vec_a: Vector, vec_b: Vector):
        vec_a += 2
        assert vec_a == Vector(5, 6)
    
    def test_addition_inplace(self, vec_a: Vector, vec_b: Vector):
        vec_a += vec_b
        assert vec_a == Vector(4, 2)
    
    def test_addition_rejects_invalid_type(self, vec_a: Vector):
        with pytest.raises(TypeError):
            _ = vec_a + "invalid"
    
    def test_radd_rejects_invalid_type(self, vec_a: Vector):
        with pytest.raises(TypeError):
            _ = "invalid" + vec_a

    # ===== SUBTRACTION =====
    def test_componentwise_subtraction(self, vec_a: Vector, vec_b: Vector):
        assert vec_a - vec_b == Vector(2, 6)
    
    def test_scalar_subtraction(self, vec_a: Vector, vec_b: Vector):
        assert vec_a - 2 == Vector(1, 2)
        assert 2 - vec_a == Vector(-1, -2)
    
    def test_scalar_subtraction_inplace(self, vec_a: Vector, vec_b: Vector):
        vec_a -= 2
        assert vec_a == Vector(1, 2)
    
    def test_subtraction_inplace(self, vec_a: Vector, vec_b: Vector):
        vec_a -= vec_b
        assert vec_a == Vector(2, 6)
    
    def test_subtraction_rejects_invalid_type(self, vec_a: Vector):
        with pytest.raises(TypeError):
            _ = vec_a - "invalid"
    
    def test_rsub_rejects_invalid_type(self, vec_a: Vector):
        with pytest.raises(TypeError):
            _ = "invalid" - vec_a

    # ===== MULTIPLICATION =====
    def test_componentwise_multiplication(self, vec_a: Vector, vec_b: Vector):
        assert vec_a * vec_b == Vector(3, -8)
    
    def test_scalar_multiplication(self, vec_a: Vector, vec_b: Vector):
        assert vec_a * 2 == Vector(6, 8)
        assert 2 * vec_a == Vector(6, 8)
    
    def test_scalar_multiplication_inplace(self, vec_a: Vector, vec_b: Vector):
        vec_a *= 2
        assert vec_a == Vector(6, 8)
    
    def test_multiplication_inplace(self, vec_a: Vector, vec_b: Vector):
        vec_a *= vec_b
        assert vec_a == Vector(3, -8)
    
    def test_mul_rejects_invalid_type(self, vec_a: Vector):
        with pytest.raises(TypeError):
            _ = vec_a * "invalid"
    
    def test_rmul_rejects_invalid_type(self, vec_a: Vector):
        with pytest.raises(TypeError):
            _ = "invalid" * vec_a

    # ===== DIVISION =====
    def test_componentwise_division(self, vec_a: Vector, vec_b: Vector):
        assert vec_a / vec_b == Vector(3 / 1, 4 / -2)
    
    def test_scalar_division(self, vec_a: Vector, vec_b: Vector):
        assert vec_a / 2 == Vector(3 / 2, 4 / 2)
        assert 2 / vec_a == Vector(2 / 3, 2 / 4)
    
    def test_scalar_division_inplace(self, vec_a: Vector, vec_b: Vector):
        vec_a /= 2
        assert vec_a == Vector(3 / 2, 4 / 2)
    
    def test_division_inplace(self, vec_a: Vector, vec_b: Vector):
        vec_a /= vec_b
        assert vec_a == Vector(3 / 1, 4 / -2)

    def test_rtruediv_rejects_invalid_type(self, vec_a: Vector):
        with pytest.raises(TypeError):
            _ = vec_a / "invalid"
    
    def test_truediv_rejects_invalid_type(self, vec_a: Vector):
        with pytest.raises(TypeError):
            _ = "invalid" / vec_a