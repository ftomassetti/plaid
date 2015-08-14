from flask import Blueprint
from flask import render_template, g
from flask import request

from app.models import Project, Tag

bp = Blueprint('project', __name__, url_prefix='/project/<project_name>')


@bp.url_value_preprocessor
def get_project(endpoint, values):
    project_name = values.pop('project_name')
    g.project = Project.query.filter_by(name=project_name).first_or_404()


@bp.url_defaults
def add_project(endpoint, values):
    if 'project_name' in values or not g.project:
        return
    values['project_name'] = g.project.name


@bp.route('/')
def index():
    stale_page = request.args.get('stale_page')
    if not stale_page:
        stale_page = 1
    else:
        stale_page = int(stale_page)
    new_page = request.args.get('new_page')
    if not new_page:
        new_page = 1
    else:
        new_page = int(new_page)
    return render_template('project.html',
                           title="Project %s" % g.project.name, stale_page=stale_page, new_page=new_page)


@bp.route('/patches/')
@bp.route('/patches/<group>')
def patches(group=None):
    if group:
        patches = getattr(g.project, group+"_patches", [])
    else:
        group = 'patches'
        patches = g.project.patches
    return render_template('project_list.html',
                           title="Project %s" % g.project.name,
                           patches=patches,
                           group=group)


@bp.route('/tag/')
def tags():
    tags = g.project.tags
    return render_template('tags.html',
                           title="All tags",
                           tags=tags)


@bp.route('/tag/<tag_name>')
def tag(tag_name):
    tags = g.project.tags

    tag = tags.filter(Tag.name == tag_name).first_or_404()
    patches = tag.patches.filter_by(project_id=g.project.id)
    return render_template('tag.html',
                           title="Tag %s" % tag.name,
                           patches=patches,
                           tag=tag)


@bp.route('/series/<series_id>')
def series(series_id=None):
    return "TODO"


@bp.route('/admin')
def admin():
    return "TODO"
