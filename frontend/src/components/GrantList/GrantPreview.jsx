import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

const mapDispatchToProps = () => ({
  favorite: () => (
    // eslint-disable-next-line no-console
    console.log('fav!')
  ),
});

const GrantPreview = (props) => {
  const { grant } = props;

  const { title, slug, author } = grant;

  return (
    <div>
      <p>{`title: ${title}`}</p>
      <p>{`slug: ${slug}`}</p>
      <p>{`author: ${author.username}`}</p>
    </div>
  );
};

export default connect(() => ({}), mapDispatchToProps)(GrantPreview);
