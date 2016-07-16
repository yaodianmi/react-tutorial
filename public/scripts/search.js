
var BookRow = React.createClass({
  render: function() {
    return (
      <tr>
        <td>
          <img src={this.props.Book.image} alt="book" height="150" width="150" />
        </td>
        <td>{this.props.Book.name}</td>
        <td>{this.props.Book.author}</td>
        <td>{this.props.Book.star}</td>
      </tr>
    );
  }
});

var BookTable = React.createClass({
  render: function() {
    var rows = [];
    this.props.books.forEach(function(Book) {
      if (Book.name.indexOf(this.props.filterText) === -1) {
        return;
      }
      rows.push(<BookRow Book={Book} key={Book.name} />);
    }.bind(this));
    return (
      <table>
        <tbody>{rows}</tbody>
      </table>
    );
  }
});

var SearchBar = React.createClass({
  handleChange: function() {
    this.props.onUserInput(
      this.refs.filterTextInput.value,
      this.refs.in8StarOnlyInput.checked
    );
  },
  render: function() {
    return (
      <form>
        <input
          type="text"
          placeholder="请输入关键词"
          value={this.props.filterText}
          ref="filterTextInput"
          onChange={this.handleChange}
        />
        <p>
          <input
            type="checkbox"
            checked={this.props.in8StarOnly}
            ref="in8StarOnlyInput"
            onChange={this.handleChange}
          />
          {' '}
          8星以上
        </p>
      </form>
    );
  }
});

var FilterableBookTable = React.createClass({
  handleBookSubmit: function(book) {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      type: 'POST',
      data: book,
      success: function(data) {
        this.setState({books: data});
      }.bind(this),
      error: function(xhr, status, err) {
        this.setState({books: book});
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getInitialState: function() {
    return {
      filterText: '',
      in8StarOnly: false,
      books: []

    };
  },
  handleUserInput: function(filterText, in8StarOnly) {
    this.setState({
      filterText: filterText,
      in8StarOnly: in8StarOnly
    });
    this.handleBookSubmit({
      'filterText': filterText,
      'in8StarOnly': in8StarOnly
    });
  },

  render: function() {
    return (
      <div>
        <SearchBar
          filterText={this.state.filterText}
          in8StarOnly={this.state.in8StarOnly}
          onUserInput={this.handleUserInput}
        />
        <BookTable
          books={this.state.books}
          filterText={this.state.filterText}
          in8StarOnly={this.state.in8StarOnly}
        />
      </div>
    );
  }
});


ReactDOM.render(
  <FilterableBookTable url="/api/db_book_search" />,
  document.getElementById('container')
);
