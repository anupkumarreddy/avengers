var data = [
    {
        'category': 'User_Management',
        'apps': [
            {
                'id': '0',
                'name': 'Ebonay Maw',
                'version': '1.0',
                'state': 'stable',
                'progress': '40',
                'license': '58'
            },
            {
                'id': '1',
                'name': 'Thanos',
                'version': '2.0',
                'state': 'beta',
                'progress': '20',
                'license': '62'
            },
            {
                'id': '2',
                'name': 'Juggernaus',
                'version': '4.0',
                'state': 'stable',
                'progress': '80',
                'license': '80'
            }
        ]
    },
    {
        'category': 'Stock_Analysis',
        'apps': [
            {
                'id': '3',
                'name': 'Magneto',
                'version': '1.0',
                'state': 'alpha',
                'progress': '60',
                'license': '44'
            },
            {
                'id': '4',
                'name': 'Dead Pool',
                'version': '3.0',
                'state': 'beta',
                'progress': '40',
                'license': '90'
            },
            {
                'id': '5',
                'name': 'Shaw Sabastian',
                'version': '4.0',
                'state': 'stable',
                'progress': '70',
                'license': '67'
            },
            {
                'id': '6',
                'name': 'Pheonix',
                'version': '5.0',
                'state': 'stable',
                'progress': '10',
                'license': '55'
            },
            {
                'id': '7',
                'name': 'Storm',
                'version': '1.0',
                'state': 'stable',
                'progress': '90',
                'license': '50'
            }
        ]
    },
    {
        'category': 'Finance',
        'apps': [
            {
                'id': '0',
                'name': 'Ebonay Maw',
                'version': '1.0',
                'state': 'stable',
                'progress': '40',
                'license': '58'
            },
            {
                'id': '1',
                'name': 'Thanos',
                'version': '2.0',
                'state': 'beta',
                'progress': '20',
                'license': '62'
            },
            {
                'id': '2',
                'name': 'Juggernaus',
                'version': '4.0',
                'state': 'stable',
                'progress': '80',
                'license': '80'
            }
        ]
    },
    {
        'category': 'User_temp',
        'apps': [
            {
                'id': '0',
                'name': 'Ebonay Maw',
                'version': '1.0',
                'state': 'stable',
                'progress': '40',
                'license': '58'
            },
            {
                'id': '1',
                'name': 'Thanos',
                'version': '2.0',
                'state': 'beta',
                'progress': '20',
                'license': '62'
            },
            {
                'id': '2',
                'name': 'Juggernaus',
                'version': '4.0',
                'state': 'stable',
                'progress': '80',
                'license': '80'
            }
        ]
    }
];

var body = d3.select("body").style("font-family", "'Oxygen', sans-serif")
    .style('font-size', '13px')
    .style('padding-top', '50px');


var container = body.append('div').attr('class', 'container apps-div');

container.selectAll('div').data(data).enter().append('div')
    .attr('class', 'row ')
    /*.attr('id', function (d) {
        return d.category;
    })*/
    .each(function () {
        var p = d3.select(this).append('div').attr('class', 'row')
            .append('div')
            .attr('class', 'col-sm-12 ')
            /*.style('border-top', '1px solid grey')*/
            .append('p')
            .attr('class', '')
            .style('padding', '5px')
            .style('border-bottom', '1px solid grey')
            .style('background', 'lavender')
            .text(function (d) {
                return d.category;
            });

        d3.select(this).append('div').attr('class', 'row ').style('margin-top', '5px')
            .attr('id', function (d) {
                return d.category;
            })
            .append('div')
            .attr('class', 'col-sm-7 col-sm-offset-1').append('div')
            .attr('class', '').append('table')
            .attr('id', 'mytable')
            .attr('class', 'table table-hover').append('tbody').selectAll('tr').data(
            function (d) {
                return d.apps;
            }).enter().append('tr').each(function () {
            d3.select(this).append('td').text(
                function (d) {
                    return d.name;
                }
            ).attr('class', 'col-sm-2');
            d3.select(this).append('td').attr('class', 'col-sm-1').append('span')
                .text(
                    function (d) {
                        return 'version : ' + d.version ;
                    }
                ).attr('class', 'label label-primary');
            d3.select(this).append('td').attr('class', 'col-sm-1').append('span')
                .style('background-color', 'lightgrey')
                .attr('class', 'badge')
                .text(
                    function (d) {
                        return d.progress + '%';
                    }
                );
            d3.select(this).append('td').text(
                function (d) {
                    return '[' + d.state + ']';
                }
            ).attr('class', 'col-sm-1');
            d3.select(this).append('td').attr('class', 'col-sm-1').append('div')
                .attr('class', 'progress').append('div')
                .attr('class', function (d) {
                    if (d.license > 50)
                        return 'progress-bar progress-bar-striped active progress-bar-success';
                    else return 'progress-bar progress-bar-striped active progress-bar-danger';
                })
                .attr('role', 'progressbar')
                .attr('aria-valuenow', '50')
                .attr('aria-valuemin', '0')
                .attr('aria-valuemax', '365')
                .style('text-align', 'center')
                .style('width', function (d) {
                    return (+d.license + 1) % 100 + '%';
                }).append('span')
                .text(
                    function (d) {
                        return d.license ;
                    }
                );
        })
        p.on("click", function (d) {
            d3.select("#" + d.category).style('display', function (d) {
                if (d3.select(this).style('display') == 'none') {
                    //console.log(d3.select(this).style('display'));
                    return 'block';
                }
                else {
                    //console.log(d3.select(this).style('display'));
                    return 'none';
                }
            })
        });
    });





