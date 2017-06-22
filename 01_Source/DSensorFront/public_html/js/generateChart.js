/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

                var chart = c3.generate({
                    bindto: '#chart',
                    data: {
                        columns: [
                            ['湿度の推移', 35.4, 100, 50.0, 70.2, 11.1, 25.6, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
                        ]
                    },
                    axis: {
                        x: {
                            label: {
                                text: '日時',
                                position: 'outer-middle'
                            }
                        },
                        y: {
                            label: {
                                text: '湿度(%)',
                                position: 'outer-middle'
                            }
                        }
                    }
                });