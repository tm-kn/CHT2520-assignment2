const path = require('path');

const STATIC_DIR = path.join(path.resolve(__dirname), 'timetracker', 'static');
const JS_DIR = path.join(STATIC_DIR, 'js')
const SCSS_DIR = path.join(STATIC_DIR, 'scss')
const OUTPUT_JS_DIR = path.join(path.resolve(__dirname), 'static_compiled', 'js')


module.exports = {
    entry: [
        path.join(SCSS_DIR, 'main.scss'),
        path.join(JS_DIR, 'index.js'),
    ],
    output: {
        filename: 'main.js',
        path: OUTPUT_JS_DIR
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /(node_modules)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader'],
            },
            {
                test: /\.scss$/,
                use: [
                    'style-loader',
                    'css-loader',
                    'sass-loader'
                ]
            }
        ]
    },
    resolve: {
        alias: {
            '@components': path.join(JS_DIR, 'components'),
        }
    },
};
