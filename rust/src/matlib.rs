use std::f64::consts::PI;

pub fn matrix_product(a: &Vec<Vec<f64>>, b: &Vec<Vec<f64>>) -> Vec<Vec<f64>> {
    let n = a.len();
    let m = a[0].len();
    let p = b[0].len();

    let mut result = vec![vec![0.0; p]; n];

    for i in 0..n {
        for j in 0..p {
            for k in 0..m {
                result[i][j] += a[i][k] * b[k][j];
            }
        }
    }

    result
}

pub fn matrix_vector_product(a: &Vec<Vec<f64>>, v: &Vec<f64>) -> Vec<f64> {
    let n = a.len();
    let m = a[0].len();

    let mut result = vec![0.0; n];

    for i in 0..n {
        for j in 0..m {
            result[i] += a[i][j] * v[j];
        }
    }

    result
}

fn invert_matrix(matrix: Vec<Vec<f64>>) -> Option<Vec<Vec<f64>>> {
    let n = matrix.len();

    // Ensure the matrix is square
    if !matrix.iter().all(|row| row.len() == n) {
        return None;
    }

    let mut a = matrix.clone();
    let mut b: Vec<Vec<f64>> = (0..n)
        .map(|i| {
            let mut row = vec![0.0; n];
            row[i] = 1.0;
            row
        })
        .collect();

    for i in 0..n {
        let mut pivot = i;
        for j in i + 1..n {
            if a[j][i].abs() > a[pivot][i].abs() {
                pivot = j;
            }
        }

        if a[pivot][i] == 0.0 {
            return None;
        }

        a.swap(i, pivot);
        b.swap(i, pivot);

        let inv_pivot = 1.0 / a[i][i];
        for j in 0..n {
            a[i][j] *= inv_pivot;
            b[i][j] *= inv_pivot;
        }

        for j in 0..n {
            if i != j {
                let factor = a[j][i];
                for k in 0..n {
                    a[j][k] -= factor * a[i][k];
                    b[j][k] -= factor * b[i][k];
                }
            }
        }
    }

    Some(b)
}

pub fn translation_matrix(x: f64, y: f64, z: f64) -> Vec<Vec<f64>> {
    vec![
        vec![1.0, 0.0, 0.0, x],
        vec![0.0, 1.0, 0.0, y],
        vec![0.0, 0.0, 1.0, z],
        vec![0.0, 0.0, 0.0, 1.0],
    ]
}

pub fn scale_matrix(x: f64, y: f64, z: f64) -> Vec<Vec<f64>> {
    vec![
        vec![x, 0.0, 0.0, 0.0],
        vec![0.0, y, 0.0, 0.0],
        vec![0.0, 0.0, z, 0.0],
        vec![0.0, 0.0, 0.0, 1.0],
    ]
}

pub fn rotate_matrix(pitch: f64, yaw: f64, roll: f64) -> Vec<Vec<f64>> {
    let pitch = pitch * PI / 180.0;
    let yaw = yaw * PI / 180.0;
    let roll = roll * PI / 180.0;

    let pitch_mat = vec![
        vec![1.0, 0.0, 0.0, 0.0],
        vec![0.0, pitch.cos(), -pitch.sin(), 0.0],
        vec![0.0, pitch.sin(), pitch.cos(), 0.0],
        vec![0.0, 0.0, 0.0, 1.0],
    ];

    let yaw_mat = vec![
        vec![yaw.cos(), 0.0, yaw.sin(), 0.0],
        vec![0.0, 1.0, 0.0, 0.0],
        vec![-yaw.sin(), 0.0, yaw.cos(), 0.0],
        vec![0.0, 0.0, 0.0, 1.0],
    ];

    let roll_mat = vec![
        vec![roll.cos(), -roll.sin(), 0.0, 0.0],
        vec![roll.sin(), roll.cos(), 0.0, 0.0],
        vec![0.0, 0.0, 1.0, 0.0],
        vec![0.0, 0.0, 0.0, 1.0],
    ];

    matrix_product(&matrix_product(&pitch_mat, &yaw_mat), &roll_mat)
}
