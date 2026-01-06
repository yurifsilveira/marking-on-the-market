function rolling(data, wind) {
    let result = [];

    for (let i = 0; i < data.length; i++) {
        if (i < wind - 1) {
            result.push(null); 
        } else {
            let add = 0;
            for (let j = 0; j < wind; j++) {
                add += data[i - j];
            }
            result.push(add / wind);
        }
    }

    return result;
}
